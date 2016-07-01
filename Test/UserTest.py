import unittest, socket, sys, time, json
from User import User
from thread import *


def setupServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print("Socket created")
    try:
        sock.bind(('0.0.0.0', port))
    except socket.error as e:
        print("Failed to bind socket. Error: " + str(e[0]) + " , " + e[1])
        print("Terminating program")
        sys.exit(-1)
    sock.listen(1)
    return sock

def connectClient(port):
    time.sleep(1)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('0.0.0.0', port))
    # print('client connected')
    sock.close()

def recieveClient(port, message):
    time.sleep(2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('0.0.0.0', port))
    # print("client connected")
    data = sock.recv(2048)
    message['data'] = data
    time.sleep(1)
    sock.close()

def tearDownServer(sock):
    sock.close()

def tearDownClient(sock):
    sock.close()

class UserTest(unittest.TestCase):
    def test1_UserCreation1(self):
        print("testUserCreation1")
        sock = setupServer(2000)
        start_new_thread(connectClient, (2000,))
        conn, addr = sock.accept()
        user1 = User(name="User", connection=conn, address=addr, id=0)
        tearDownServer(sock)
        self.assertTrue(True)

    def test2_UserCreation2(self):
        print("testUserCreation2")
        sock = setupServer(3000)
        start_new_thread(connectClient, (3000,))
        conn, addr = sock.accept()
        user1 = User(name="User", connection=conn, address=addr, id=0)
        tearDownServer(sock)
        self.assertTrue(True)

    def test3_UserName1(self):
        print("testUserName1")
        sock = setupServer(2010)
        start_new_thread(connectClient, (2010,))
        conn, addr = sock.accept()
        user1 = User(name="User", connection=conn, address=addr, id=0)
        tearDownServer(sock)
        self.assertEqual(user1.__str__(), "name : User")

    def test4_UserCompare1(self):
        print("testUserCompare2")
        sock = setupServer(2020)
        start_new_thread(connectClient, (2020,))
        conn, addr = sock.accept()
        user1 = User(name="User", connection=conn, address=addr, id=0)
        self.assertTrue(user1 == user1)
        tearDownServer(sock)

    def test5_UserCompare2(self):
        print("testUserCompare2")
        sock1 = setupServer(2020)
        start_new_thread(connectClient, (2020,))
        conn1, addr1 = sock1.accept()
        user1 = User(name="User1", connection=conn1, address=addr1, id=0)
        sock2 = setupServer(2030)
        start_new_thread(connectClient, (2030,))
        conn2, addr2 = sock2.accept()
        user2 = User(name="User2", connection=conn2, address=addr2, id=1)
        self.assertFalse(user1 == user2)
        tearDownServer(sock1)
        tearDownServer(sock2)

    def test6_UserSend1(self):
        print("testUserSend1")
        user = User(name="User", connection=None, address=None, id=0)
        try:
            user.sendMessage("Hi!")
        except UnboundLocalError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test7_UserSend2(self):
        print("testUserSend2")
        sock1 = setupServer(2040)
        message = dict()
        start_new_thread(recieveClient, (2040, message))
        conn1, addr1 = sock1.accept()
        # print("connection accepted")
        user1 = User(name="User1", connection=conn1, address=addr1, id=0)
        data = "hi!"
        user1.sendMessage(data)
        found = False
        for i in range(0, 10000):
            if message.has_key('data'):
                self.assertTrue(message['data'] == data)
                found = True
                break
        if not found:
            self.assertTrue(False)
        tearDownServer(sock1)

    def test8_UserSend3(self):
        print("testUserSend3")
        sock1 = setupServer(2040)
        message = dict()
        start_new_thread(recieveClient, (2040, message))
        conn1, addr1 = sock1.accept()
        # print("connection accepted")
        user1 = User(name="User1", connection=conn1, address=addr1, id=0)
        data = dict()
        data['status'] = 'test'
        data['other'] = 'more data here'
        dataJson = json.dumps(data)
        user1.sendMessage(dataJson)
        found = False
        for i in range(0, 10000):
            if message.has_key('data'):
                self.assertTrue(message['data'] == dataJson)
                found = True
                break
        if not found:
            self.assertTrue(False)
        tearDownServer(sock1)


if __name__ == '__main__':
    unittest.main()

