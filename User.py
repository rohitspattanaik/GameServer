import json, socket

class User:
    'Used by the game server to keep track of its clients'
    name = ""
    connection, address = None, None

    def __init__(self, *args, **kwargs):
        name = kwargs.get('name')
        connection = kwargs.get('connection')
        address = kwargs.get('address')


    def __str__(self):
        print("name : " + str(self.name))
        print("connection : " + str(self.connection))
        print("address : " + str(self.address))


    def sendMessage(self, returnMessage):
        if self.connection == None:
            raise UnboundLocalError("user connection not popluated")

        connection.sendall(json.dumps(returnMessage))



