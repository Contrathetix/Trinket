import os
import logging
import subprocess

import shared.modulebase


class Game(shared.modulebase.ModuleBase):

    def preferred_load_index(self) -> int:
        return 4

    def run_and_wait(self):
        eso_path = self.app.config.get('game.path')
        eso_exe = self.app.config.get('game.exe')
        command = [os.path.join(eso_path, eso_exe)]
        os.chdir(eso_path)
        process = subprocess.Popen(command)
        process.wait()

    def run_and_do_not_wait(self):
        eso_path = self.app.config.get('game.path')
        eso_exe = self.app.config.get('game.exe')
        logging.info('chdir to \'{}\''.format(eso_path))
        os.chdir(eso_path)
        logging.info('startfile \'{}\''.format(eso_exe))
        os.startfile(os.path.join(eso_path, eso_exe))
