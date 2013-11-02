import flask
import random
import string
import json
import time
import functools

from flask.ext.sqlalchemy import SQLAlchemy


app = flask.Flask(__name__)
app.config.from_object('config.RunningConfig')
db = SQLAlchemy(app)


import model
import games
import execution

def _generate_hash():
    return ''.join(random.choice(string.letters + string.digits) for _ in range(8))


def ev_level(l):
    desc, comm = games.LEVELS[l-1]
    return (0, time.time(), "Welcome to level {}. If you're unlucky, the script will {}.".format(l, desc))

@app.route('/')
def index():
    hash = _generate_hash()
    events = []
    events.append((0, time.time(), 'Game {} started.'.format(hash)))
    events.append(ev_level(1))
    g = model.Game(hash=hash, level=1, events=json.dumps(events), shots=6)
    db.session.add(g)
    db.session.commit()
    return flask.redirect('/i/' + hash)


@app.route('/i/<hash>')
def hash_info(hash):
    g = model.Game.query.filter_by(hash=hash).first()
    if g is None:
        return "no such game."
    events = json.loads(g.events)
    description, command = games.LEVELS[g.level-1]
    return flask.render_template('base.html', hash=g.hash, level=g.level,
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
        if 'hash' in kwargs and 'username' in kwargs:
            g = model.Game.query.filter_by(hash=kwargs['hash']).first()
            if g is not None:
                events = json.loads(g.events)
                events.append((2, time.time(), kwargs['username'] + ' chickened out and tried to take a sneak peek via ' + agent))
                g.events = json.dumps(events)
                db.session.commit()
        if 'curl' in agent.lower():
            return f(*args, **kwargs)
        else:
            return "Curl me to shell if you dare."
    return wrapper

@app.route('/h/<hash>/<username>')
@curlonly
def hash_execute(hash, username):
    g = model.Game.query.filter_by(hash=hash).first()
    if g is None:
        return ex(execution.nohash())
    description, command = games.LEVELS[g.level-1]
    if random.random() < (1.0/g.shots):
        # bang!
        return execution.bang(hash, g.level, command, username)
    else:
        # click!
        return execution.click(hash, g.level, command, username)

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
    db.session.commit()
    return ''

@app.route('/e/<hash>')
def get_events(hash):
    g = model.Game.query.filter_by(hash=hash).first()
    if g is None:
        return flask.jsonify([])
    return flask.jsonify(events=json.loads(g.events))
    

if __name__ == '__main__':
    app.run(debug=True)
