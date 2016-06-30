import unittest, socket, sys, time
from User import User
from thread import *


def setupServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created")
    try:
        sock.bind(('0.0.0.0', port))
    except socket.error as e:
        print("Failed to bind socket. Error: " + str(e[0]) + " , " + e[1])
        print("Terminating program")
        sys.exit(-1)
    sock.listen(1)
    return sock

def connectClient(port):
    time.sleep(2)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('0.0.0.0', port))
    print('client connected')
    sock.close

def tearDownServer(sock):
    sock.close()

def tearDownClient(sock):
    sock.close()

class tUserTest(unittest.TestCase):
    def testUserCreation1(self):
        sock = setupServer(2000)
        start_new_thread(connectClient, (2000,))
        conn, addr = sock.accept()
        user1 = User(name="User", connection=conn, address=addr, id=0)
        tearDownServer(sock)
        self.assertTrue(True)

    def testUserCreation2(self):
        sock = setupServer(3000)
        start_new_thread(connectClient, (3000,))
        conn, addr = sock.accept()
        user1 = User(name="User", connection=conn, address=addr, id=0)
        tearDownServer(sock)
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()

