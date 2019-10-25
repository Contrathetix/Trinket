import os
import inspect
import shutil
import shared.modulebase


class Cleanup(shared.modulebase.ModuleBase):

    def preferred_load_index(self) -> int:
        return 10

    def on_load(self) -> None:
        self.cleanup_folders = self.app.config.get('cleanup.folders')
        self.start_path = self.app.path

    def on_unload(self) -> None:
        self.recursive_clean(self.start_path)

    def recursive_clean(self, path: str) -> None:
        for fp in os.scandir(path):
            if fp.name in self.cleanup_folders:
                shutil.rmtree(fp.path)
            elif os.path.isdir(fp.path) and not fp.name.startswith('.'):
                self.recursive_clean(fp.path)
