from decouple import config
import socket
class TwitchBot():
    
    serveur = "irc.chat.twitch.tv"
    port = 6667
    nickname = "appez"
    token = config('TWITCH_TOKEN')
    channel = "#rs_appez"

    def __init__(self):
        self.connect()

        while True:
            response = self.irc.recv(2048).decode("utf-8")
            if response.startswith("PING"):
                self.irc.send("PONG\n".encode("utf-8"))
            else:
                if "test" in response:
                    self.irc.send(f"PRIVMSG {self.channel} :test\n".encode("utf-8"))
                print(response)

    def connect(self):
        self.irc = socket.socket()
        self.irc.connect((self.serveur, self.port))
        self.irc.send(f"PASS {self.token}\n".encode("utf-8"))
        self.irc.send(f"NICK {self.nickname}\n".encode("utf-8"))
        self.irc.send(f"JOIN {self.channel}\n".encode("utf-8"))