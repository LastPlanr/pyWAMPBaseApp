from concurrent.futures import ThreadPoolExecutor
import asyncio
import sys

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from autobahn.wamp.auth import compute_wcs
from autobahn.wamp.types import RegisterOptions
from autobahn.wamp.exception import ApplicationError
from prettyconf import config


def register_method(name, **options):
    def decorator(method):
        method.wamp_name = name
        method.wamp_options = options
        return method
    return decorator


class WampApp(ApplicationSession):
    PRINCIPAL = None
    METHODS_SUFFIX = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exit_status = 0
        self.init()
        self.methods = {}
        self.thread_pool_executor = ThreadPoolExecutor()

        for thing_name in dir(self):
            thing = getattr(self, thing_name)
            method_name = getattr(thing, 'wamp_name', None)
            if method_name:
                self.methods[method_name] = (thing, thing.wamp_options)

    def init(self):
        pass

    def onOpen(self, *args, **kwargs):
        print('Opened.')
        super().onOpen(*args, **kwargs)

    def onWelcome(self, *args, **kwargs):
        print('Welcome message received.')
        super().onWelcome(*args, **kwargs)

    def onConnect(self):
        print("Client session connected. Starting WAMP-Ticket authentication on realm '{}' as principal '{}' ..".format(
            self.config.realm, self.PRINCIPAL)
        )
        self.join(self.config.realm, [u"ticket"], self.PRINCIPAL)

    def onUserError(self, *args, **kwargs):
        print('onUserError:', args, ';', kwargs)
        return super().onUserError(*args, **kwargs)

    async def ready(self):
        pass

    async def onJoin(self, details):
        last_exception = None
        for counter in range(0, 3):
            if counter > 0:
                await asyncio.sleep(5)

            try:
                for method_name, method_data in self.methods.items():
                    method, method_options = method_data
                    sufixed_name = f'{method_name}{self.METHODS_SUFFIX}'

                    if method_options:
                        options = RegisterOptions(**method_options)
                        await self.register(method, sufixed_name, options)
                    else:
                        await self.register(method, sufixed_name)
            except ApplicationError as e:
                last_exception = e
                continue
            else:
                print("All methods registered")
                break
        else:
            print(f"Could not register some methods: {last_exception}")
            self.exit_status = 10
            self.disconnect()
            return

        self.loop = asyncio.get_event_loop()

        await self.ready()

    def onChallenge(self, challenge):
        secret = config('WAMPYSECRET')
        if challenge.method == u"ticket":
            print("WAMP-Ticket challenge received: {}".format(challenge))
            return secret
        elif challenge.method == u"wampcra":
            return compute_wcs(secret, challenge.extra['challenge'])
        else:
            raise Exception("Invalid authmethod {}".format(challenge.method))

    def onLeave(self, *args, **kwargs):
        # 1 - leave
        super().onLeave(*args, **kwargs)
        print('Left.')

    def onDisconnect(self):
        # 2- disconnect
        super().onDisconnect()
        print("Disconnected.")

    def onClose(self, *args, **kwargs):
        # 3- close
        super().onClose(*args, **kwargs)
        print('Closed.')
        sys.exit(self.exit_status)

    @classmethod
    def run(cls):
        url = config('WAMP_URL')
        realm = config('WAMP_REALM')

        runner = ApplicationRunner(url, realm)

        try:
            runner.run(cls)
        except OSError as ex:
            print('OSError:', ex)
            sys.exit(100)

    async def async_run(self, function, *args, **kwargs):
        return await self.loop.run_in_executor(self.thread_pool_executor, function, *args, **kwargs)
