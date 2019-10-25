class ModuleBase(object):

    def __init__(self, app) -> None:
        super().__init__()
        self.app = app

    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass

    def preferred_load_index(self) -> int:
        return 0
