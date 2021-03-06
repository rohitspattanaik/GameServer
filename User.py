import socket


class User:
    'Used by the game server to keep track of its clients'


    def __init__(self,**kwargs):
        self.name = kwargs.get('name')
        self.connection = kwargs.get('connection')
        self.address = kwargs.get('address')
        self.id = kwargs.get('id') #TODO: generate ids


    def __del__(self):
        if self.connection != None:
            self.connection.close()


    def __str__(self):
        return ("name : " + str(self.name))


    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id and self.address == other.address

    def __ne__(self, other):
        return not self == other


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
        dataDictionary[self.id] = data


    def close(self):
        self.connection.close()



