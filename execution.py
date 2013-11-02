def nohash():
    return "echo 'no such game.'"

def bang(hash, level, command, username):
    data = "#!/bin/sh\n"
    data += "( "
    data += command
    data += " ) && curl -silent http://russianroulette.sh/b/{}/{}/{}".format(hash, level, username)
    data += "\n"
    return data

def click(hash, level, command, username):
    data = "#!/bin/sh\n"
    data += "( echo 'click!' ) && curl -silent http://russianroulette.sh/c/{}/{}/{}".format(hash, level, username)
    data += "\n"
    return data
