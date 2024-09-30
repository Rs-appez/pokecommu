from decouple import config
import socket
import re
import threading
class TwitchBot():
    
    serveur = "irc.chat.twitch.tv"
    port = 6667
    nickname = "appez"
    token = config('TWITCH_TOKEN')
    channel = "#rs_appez"

    def __init__(self):

        self.__start()


    def __start(self):
        self.__connect()

        threading.Thread(target=self.__listen,name="Bot irc").start()


        while True:
            response = self.irc.recv(2048).decode("utf-8")
            if response.startswith("PING"):
                self.irc.send("PONG\n".encode("utf-8"))
            else:
                self.__parse_message(response)

    def __connect(self):
        self.irc = socket.socket()
        self.irc.connect((self.serveur, self.port))
        self.irc.send(f"PASS {self.token}\n".encode("utf-8"))
        self.irc.send(f"NICK {self.nickname}\n".encode("utf-8"))
        self.irc.send(f"JOIN {self.channel}\n".encode("utf-8"))

    def __listen(self):
        while True:
            response = self.irc.recv(2048).decode("utf-8")
            if response.startswith("PING"):
                self.irc.send("PONG\n".encode("utf-8"))
            else:
                self.__parse_message(response)

    def __parse_message(self, message):
        r = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', message)
        if r:
            username, channel, message = r.groups()
            print(username + ": " + message)

    
