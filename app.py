import flask
import random
import string
import json
import time
import functools
import memcache

from flask.ext.sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.config.from_object('config.RunningConfig')
db = SQLAlchemy(app)
mc = memcache.Client(['127.0.0.1:11211'], debug=0)

import model
import games
import execution

def _generate_hash():
    return ''.join(random.choice(string.letters + string.digits) for _ in range(8))


def ev_level(l):
    try:
        desc, comm = games.LEVELS[l-1]
    except IndexError:
        desc, comm = games.LEVELS[-1]
    return (0, time.time(), "Welcome to level {}. If you're unlucky, the script will {}.".format(l, desc))

def encache(g):
    hash = g.hash
    level = g.level
    events = g.events
    shots = g.shots
    mc.set('l-' + hash.encode('ascii'), level, time=3600)
    mc.set('e-' + hash.encode('ascii'), events, time=3600)
    mc.set('s-' + hash.encode('ascii'), shots, time=3600)

@app.route('/')
def index():
    hash = _generate_hash()
    events = []
    events.append((0, time.time(), 'Game {} started.'.format(hash)))
    events.append(ev_level(1))
    g = model.Game(hash=hash, level=1, events=json.dumps(events), shots=6)
    db.session.add(g)
    db.session.commit()
    encache(g)
    return flask.redirect('/i/' + hash)


@app.route('/i/<hash>')
def hash_info(hash):
    events = mc.get('e-' + hash.encode('ascii'))
    level = mc.get('l-' + hash.encode('ascii'))
    if not level or not events:
        g = model.Game.query.filter_by(hash=hash).first()
        if g is None:
            return "no such game."
        encache(g)
        events = g.events
        level = g.level
    events = json.loads(events)
    try:
        description, command = games.LEVELS[level-1]
    except IndexError:
        desc, comm = games.LEVELS[-1]
    return flask.render_template('base.html', hash=hash, level=level,
                                 punishement=description, events=events)

@app.route('/about')
def about():
    return flask.render_template('about.html')

def ex(t):
    return flask.Response(t, mimetype='text/x-shellscript')

def curlonly(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        agent = flask.request.headers.get('User-Agent')
        if 'hash' in kwargs and 'username' in kwargs and 'curl' not in agent.lower():
            g = model.Game.query.filter_by(hash=kwargs['hash']).first()
            if g is not None:
                events = json.loads(g.events)
                events.append((2, time.time(), kwargs['username'] + ' chickened out and tried to take a sneak peek via ' + agent))
                g.events = json.dumps(events)
                encache(g)
                db.session.commit()
        if 'curl' in agent.lower():
            return f(*args, **kwargs)
        else:
            return "Curl me to shell if you dare."
    return wrapper

@app.route('/h/<hash>/<username>')
@curlonly
def hash_execute(hash, username):
    level = mc.get('l-' + hash.encode('ascii'))
    shots = mc.get('s-' + hash.encode('ascii'))
    if None in (level, shots):
        g = model.Game.query.filter_by(hash=hash).first()
        if g is None:
            return ex(execution.nohash())
        encache(g)
        level = g.level
        shots = g.shots
    try:
        description, command = games.LEVELS[level-1]
    except IndexError:
        desc, comm = games.LEVELS[-1]
    if random.random() < (1.0/shots):
        # bang!
        return execution.bang(hash, level, command, username)
    else:
        # click!
        return execution.click(hash, level, command, username)

@app.route('/c/<hash>/<int:level>/<username>')
@curlonly
def click(hash, username, level):
    g = model.Game.query.filter_by(hash=hash).first()
    if g is None:
        return ""
    if g.level != level:
        return ""
    events = json.loads(g.events)
    if g.shots < 2:
        events.append((0, time.time(), username + ' clicked event though there was one bullet left... race condition?'))
    else:
        events.append((1, time.time(), username + ' *click*'))
        g.shots -= 1
    g.events = json.dumps(events)
    encache(g)
    db.session.commit()
    return ''

@app.route('/b/<hash>/<int:level>/<username>')
@curlonly
def bang(hash, username, level):
    g = model.Game.query.filter_by(hash=hash).first()
    if g is None:
        return "no game"
    if g.level != level:
        return "wrong level {} {}".format(g.level, level)
    g.shots = 6
    events = json.loads(g.events)
    events.append((3, time.time(), username + ' *BANG!*'))
    events.append(ev_level(g.level+1))
    g.events = json.dumps(events)
        
    g.level += 1
    encache(g)
    db.session.commit()
    return ''

@app.route('/e/<hash>')
def get_events(hash):
    events = mc.get('e-' + hash.encode('ascii'))
    if not events:
        g = model.Game.query.filter_by(hash=hash).first()
        if g is None:
            return flask.jsonify([])
        encache(g)
        events = g.events
    return flask.jsonify(events=json.loads(events))
    

if __name__ == '__main__':
    app.run(debug=True)
