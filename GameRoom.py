import socket, json, string, random
import masterConfig, errorCodes


class GameRoom:
    'Where a game is hosted'
    roomNames = []


    def __init__(self, *args, **kwargs):
        self.name = ''
        self.users = []
        self.socket = socket()


    def __str__(self):
        return self.name


    def generateErrorMessage(self, message):
        print(message)


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
            self.socket.bind((masterConfig.host, roomPort))
        except socket.error as e:
            self.generateErrorMessage("Room " + self.name + " failed to bind socket")
            return errorCodes.roomSocketError

        return errorCodes.good


    def connectUser(self, user):
        if not isinstance(user, User):
            raise ValueError("User not provided to room")
        if user in users:
            self.generateErrorMessage("User " + user + " already connected to room " + self.name)
            return errorCodes.duplicateUser

        message = dict()
        message["status"] = "connect"
        message["room"] = self.name
        user.sendMessage(json.dumps(message))

        dataJson = user.receiveMessage()
        try:
            data = json.loads(dataJson)
        except ValueError:
            self.generateErrorMessage("Error parsing json in room " + self.name)
            return errorCodes.roomJsonError
        #continue this