def nohash():
    return "echo 'no such game.'"

def bang(hash, command, username):
    data = "#!/bin/sh\n"
    data += "( "
    data += command
    data += " ) && curl -silent http://russianroulette.sh/b/" + hash +'/' + username
    data += "\n"
    return data

def click(hash, command, username):
    data = "#!/bin/sh\n"
    data += "( echo 'click!' ) && curl -silent http://russianroulette.sh/c/" + hash + '/' + username
    data += "\n"
    return data
