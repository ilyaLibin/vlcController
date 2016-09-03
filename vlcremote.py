import sys
import os
import telnetlib

class VLCRemote:
    def __init__(self):
        self.host = 'localhost'
        self.tn = None

    def login(self, port, password, user=""):
        self.password = bytes(password, 'UTF-8')
        self.user = bytes(user, 'UTF-8')
        self.port = bytes(port, 'UTF-8')

        try:
            self.tn = telnetlib.Telnet(self.host, self.port)
            print(self.tn)
        except Exception as e:
            raise e
            os.system('kill $PPID')
            sys.exit(1)

        self.tn.read_until(b"Password: ")
        self.tn.write(self.password + b"\n")

    def play(self):
        if self.tn:
            self.tn.write(b'play\n')
        else:
            self.login()
            self.play()

    def pause(self):
        if self.tn:
            self.tn.write(b'pause\n')
        else:
            self.login()
            self.pause()


    def up(self):
        if self.tn:
            self.tn.write(b'volup\n')
        else:
            self.login()
            self.up()

    def down(self):
        if self.tn:
            self.tn.write(b'voldown\n')
        else:
            self.login()
            self.down()
