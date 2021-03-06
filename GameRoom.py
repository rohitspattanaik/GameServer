import socket, json, string, random, thread
import masterConfig, errorCodes, User


#should I have the room class keep track of all the rooms and the bindings, etc or delegate that to a 'lobby'...

class GameRoom:
    'Where a game is hosted'
    roomNames = []


    def __init__(self, **kwargs):
        self.name = ''
        self.users = []
        self.ip = masterConfig.host
        self.socket = socket()
        self.numberOfUsers = 1  # To accommodate host
        if kwargs.has_key("gameType"):
            self.gameType = kwargs["gameType"]
        else:
            self.gameType = "NULL"


    def __str__(self):
        return self.name


    def generateErrorMessage(self, message):
        print(message)


    def checkKeys(self, data, keys):
        for key in keys:
            if key not in data:
                return False

        return True


    def generateRoomName(self, size = 4, charSet = string.ascii_uppercase + string.digits):
        name = ''.join(random.choice(charSet) for _ in range(size))
        if name in roomNames:
            generateRoomName()
        else:
            self.name = name
            roomNames.append(self.name)


    def bindSocket(self, roomPort):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.ip, roomPort))
        except socket.error as e:
            self.generateErrorMessage("Room " + self.name + " failed to bind socket")
            return errorCodes.roomSocketError

        return errorCodes.good


    def messageRoom(self, message):
        for user in self.users:
            user.sendMessage(message)


    def connectUser(self, user):
        if len(self.users) == self.numberOfUsers:
            self.generateErrorMessage("Connection to user denied. Room " + self.name + " at capacity")
            return errorCodes.roomAtCapacity

        if not isinstance(user, User):
            raise ValueError("User not provided to room")
        if user in users:
            self.generateErrorMessage("User " + user + " already connected to room " + self.name)
            return errorCodes.duplicateUser

        message = dict()
        message["action"] = "connect"
        message["room"] = self.name
        user.sendMessage(json.dumps(message))

        dataJson = user.receiveMessage()
        try:
            data = json.loads(dataJson)
        except ValueError:
            self.generateErrorMessage("Error parsing json in room " + self.name)
            return errorCodes.roomJsonError

        if not self.checkKeys(data, ["action","status"]):
            self.generateErrorMessage("Missing tags in json")
            #TODO:notify user here?
            return errorCodes.incompleteJson

        if data["action"] != "connect":
            #TODO:SHOULD NOT PASS. This is an error case that needs to be handled
            pass

        if data["status"] != "success":
            return errorCodes.unknownRoomError

        self.users.append(user)
        return errorCodes.good


    #Not sure if I'll need this. It's here just in case
    def dropUser(self, user, message=""):
        returnMessage = dict()
        returnMessage["action"] = "drop"
        returnMessage["message"] = message
        user.sendMessage(json.dumps(returnMessage))
        self.users.remove(user)
        user.close()



    def connectUsers(self):
        returnMessage = dict()
        hostConnected = False
        allConnected = False

        while not allConnected:
            userConnection, userAddress = self.socket.accept()

            dataJson = self.socket.receive(4096)
            try:
                data = json.loads(dataJson)
            except ValueError:
                self.generateErrorMessage("Error parsing json in room " + self.name)
                return errorCodes.roomJsonError

            if not self.checkKeys(data, ["action","type","roomName","name"]):
                self.generateErrorMessage("Missing tags in json")
                #TODO:notify user here?
                return errorCodes.incompleteJson

            if data["action"] != "connect":
                #TODO: handle this case
                if data["action"] == "update" and data["type"] == "host":
                    if data.get("status") == "allGuestsConnected":
                        allConnected = True
                        continue
                pass

            if data["type"] == "guest":
                if not hostConnected:
                    #TODO: send message back to inform that host not connected
                    continue

            if data["roomName"] != self.name:
                #should never really happen. this is a server error
                #TODO: send message back that wrong room
                continue

            if data["type"] == "host":
                if not self.checkKeys(data, "numGuests"):
                    self.numberOfUsers = masterConfig.maxPlayers

                else:
                    if data["numGuests"] > masterConfig.maxPlayers or data["numGuests"] < 0:
                        num = masterConfig.maxPlayers
                    else:
                        num = data["numGuests"] + 1
                    self.numberOfUsers = num


            userArgs = dict()
            userArgs["name"] = data["name"]
            userArgs["address"] = userAddress
            userArgs["connection"] = userConnection
            user = User(userArgs)
            ret = self.connectUser(user)
            if ret != 0:
                #TODO:have better error handling
                continue

            if data["type"] == "host":
                hostConnected = True

            if len(self.users) == self.numberOfUsers:
                allConnected = True

            returnMessage.clear()
            returnMessage["action"] = "update"
            returnMessage["message"] = user.name + " connected"
            self.messageRoom(json.dumps(returnMessage))


    def getUserResponse(self):
        returnData = dict()
        for user in self.users:
            thread.start_new_thread(user.recieveMessageShared, (returnData, ))
        while len(returnData) != self.numberOfUsers:
            #busy waiting
            pass
        return returnData


