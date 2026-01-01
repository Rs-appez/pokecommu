import asyncio
import threading

from mitmproxy import http
from mitmproxy.options import Options
from mitmproxy.tools.dump import DumpMaster

from business.pokeBusiness import PokeBusiness
from pokeCommu import PokeCommu


class PokeTwitchProxy:
    class Addon:
        def __init__(self, pokeCommu: PokeCommu):
            self.pcommu = pokeCommu

        def response(self, flow: http.HTTPFlow) -> None:
            # Refresh pokedex
            if (
                flow.request.pretty_url
                == "https://poketwitch.bframework.de/api/game/ext/trainer/pokedex/v2/"
            ):
                print("refreshing pokedex from proxy...")
                response_data = flow.response.json()
                self.pcommu.load_pokedex(response_data)

            # Refresh inventory
            elif (
                flow.request.pretty_url
                == "https://poketwitch.bframework.de/api/game/ext/trainer/inventory/v3/"
            ):
                print("refreshing inventory from proxy...")
                response_data = flow.response.json()
                self.pcommu.load_inventory(response_data)

            # Refresh pokemons
            elif (
                flow.request.pretty_url
                == "https://poketwitch.bframework.de/api/game/ext/trainer/pokemon/v2/"
            ):
                print("refreshing pokemons from proxy...")
                response_data = flow.response.json()
                self.pcommu.load_pokemons(response_data)

    def __init__(self, poke_business: PokeBusiness):
        self.options = Options(
            listen_host="0.0.0.0", listen_port=15100, mode=["regular"]
        )
        self.pkb = poke_business

    async def _run_proxy(self):
        self.m = DumpMaster(self.options, with_termlog=False, with_dumper=False)
        self.m.addons.add(self.Addon(self.pkb.pokeCommu))
        print("Starting PokeTwitch Proxy on port 15100...")
        await self.m.run()

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._run_proxy())
        except KeyboardInterrupt:
            print("Stopping PokeTwitch Proxy...")
            try:
                self.m.shutdown()
            except Exception as e:
                print(f"Error during shutdown of PokeTwitch Proxy: {e}")
        finally:
            loop.close()
