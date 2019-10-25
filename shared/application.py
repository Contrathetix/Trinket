import os
import sys
import atexit
import logging
import inspect
import importlib


class Application(object):

    def __init__(self):
        super().__init__()
        self.argv = sys.argv
        self.path = os.path.abspath(os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)),
            '..'
        ))
        self.setup_logging()
        self.actionmap = {
            '--game': self.execute_game,
            '--convert-screenshots': self.convert_screenshots
        }
        self.load_modules()

    def load_modules(self) -> None:
        module_root = 'modules'
        self.modules = {}
        self.objects_list = []
        for fp in os.scandir(module_root):
            if (not fp.name.endswith('.py')):
                continue
            module_name = fp.name.replace('.py', '')
            self.modules[module_name] = importlib.import_module(
                '{}.{}'.format(module_root, module_name)
            )
            module_class = getattr(self.modules[module_name], module_name)
            module_object = module_class(self)
            module_object.load_index = module_object.preferred_load_index()
            self.objects_list.append(module_object)
        self.objects_list.sort(key=lambda x: x.preferred_load_index())
        for module_object in self.objects_list:
            atexit.register(module_object.on_unload)
            module_object.on_load()
            setattr(self, type(module_object).__name__.lower(), module_object)

    def setup_logging(self) -> None:
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s][%(levelname)-6s] %(filename)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            filename='data/action.log',
            filemode='w'
        )

    def run(self) -> None:
        logging.info('application started with {}'.format(' '.join(self.argv)))
        try:
            func = self.actionmap[self.argv[1]]
            func()
        except (KeyError, IndexError) as exc:
            logging.error(exc)

    def execute_game(self) -> None:
        logging.info('open game')
        self.ttcdata.update()
        self.game.run_and_do_not_wait()

    def convert_screenshots(self) -> None:
        logging.info('convert screenshots')
