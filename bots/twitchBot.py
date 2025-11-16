from decouple import config
import threading
import re
import websocket

from business.pokeBusiness import PokeBusiness


class TwitchBot:
    nickname = config("NICKNAME")
    token = config("TWITCH_TOKEN")
    channel = f"#{config('CHANNEL')}"

    def __init__(self, pkb: PokeBusiness):
        self.pkb = pkb
        self.session_id = None
        self.ws = None

        self.__start()

    def __start(self):
        threading.Thread(target=self.__connect, name="Bot").start()

    def __connect(self):
        self.ws = websocket.WebSocketApp(
            "wss://irc-ws.chat.twitch.tv:443",
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close,
        )
        self.ws.on_open = self.__on_open
        self.ws.run_forever()

    def __on_message(self, ws, message):
        if message.startswith("PING"):
            print("PING")
            ws.send("PONG\n")

        else:
            if message:
                self.__parse_message(message)

    def __on_error(self, ws, error):
        print(f"Error: {error}")

    def __on_close(self, ws, close_status_code, close_msg):
        print(f"code : {close_status_code}")
        print(f"msg : {close_msg}")
        print("### closed ###")

    def __on_open(self, ws):
        print("### opened ###")
        ws.send("CAP REQ :twitch.tv/membership twitch.tv/tags twitch.tv/commands")
        ws.send(f"PASS oauth:{self.token}")
        ws.send(f"NICK {self.nickname}")

        ws.send(f"JOIN {self.channel}")

        print(f"###connected to {self.channel} channel###")

    def __parse_message(self, message):
        r = re.search(r":(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)", message)
        if r:
            username, channel, message = r.groups()
            username = username.split(":")[-1]

            if username == "pokemoncommunitygame" and self.pkb:
                if "A wild" in message:
                    priority = False
                    if "TwitchLit" not in message:
                        priority = True
                    print("Un pokémon sauvage apparaît")

                    pokemon_name = ""
                    message_array = message.split(" ")[4:]

                    # handle spaces in pokemon names
                    for m in message_array:
                        if m != "appears":
                            pokemon_name += m + " "
                        else:
                            break

                    pokemon_name = pokemon_name.strip()
                    print(pokemon_name)
                    if pokemon_name == "Unidentified Ghost":
                        if self.pkb.pokeCommu.check_ball_in_inventary("ultra_ball"):
                            self.__send_message("!pokecatch ultraball")
                            return

                        self.__send_message("!pokecheck")
                        return

                    ball = self.pkb.catch_pokemon(pokemon_name, priority)
                    if ball:
                        if self.pkb.is_economic:
                            print("No catching because economic mode is on")
                            self.__send_message("!pokecheck")
                            return
                        self.__send_message(f"!pokecatch {ball}")

    def __send_message(self, message):
        if self.ws:
            self.ws.send(f"PRIVMSG {self.channel} :{message}\n")
