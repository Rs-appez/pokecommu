from decouple import config
import socket
import re
import threading

from pokeBusiness import PokeBusiness
class TwitchBot():
    
    serveur = "irc.chat.twitch.tv"
    port = 6667
    nickname = "appez"
    token = config('TWITCH_TOKEN')
    channel = "#ephemeriia"

    def __init__(self, pkb : PokeBusiness = None):
        self.pkb = pkb

        self.__start()

    def __start(self):
        self.__connect()

        threading.Thread(target=self.__listen,name="Bot irc").start()


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

            if username == "pokemoncommunitygame" and self.pkb:
                if "sauvage apparaît" in message:
                    print("Un pokémon sauvage apparaît")
                    pokemon_name = message.split(" ")[3]
                    ball = self.pkb.catch_pokemon(pokemon_name)
                    if ball:
                        self.send_message(f"!pokecatch {ball}")

    
    def send_message(self, message):
        self.irc.send(f"PRIVMSG {self.channel} :{message}\n".encode("utf-8"))
                    

    
