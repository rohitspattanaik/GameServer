import socket


class User:
    'Used by the game server to keep track of its clients'


    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.connection = kwargs.get('connection')
        self.address = kwargs.get('address')
        self.id = 0; #TODO: generate ids


    def __del__(self):
        self.connection.close()


    def __str__(self):
        return ("name : " + str(self.name))


    def __cmp__(self, other):
        if not isinstance(other, User):
            return False
        return self.name == other.name and self.address == other.address


    #Method to send a message to whatever User is connected to
    #The return message should already be in the proper format
    def sendMessage(self, returnMessage):
        if self.connection == None:
            raise UnboundLocalError("User connection not defined")

        self.connection.sendall(returnMessage)


    #blocking for now
    def receiveMessage(self):
        data = self.connection.receive(4096)
        return data


    def recieveMessageShared(self, dataDictionary):
        data = self.connection.receive(4096)
        dataDictionary[self.name] = data


    def close(self):
        self.connection.close()



