import re
import json
import logging
import datetime
import shared.modulebase


class ScreenshotMetadata(shared.modulebase.ModuleBase):

    def preferred_load_index(self) -> int:
        return 7

    def parse_vdf(self) -> None:
        path = self.app.config.get('screenshot.metadata.path')
        replacements = self.app.config.get('screenshot.metadata.regex_in')
        logging.info('open \'{}\''.format(path))
        with open(self.path, 'r') as vdf_file:
            self.vdf = vdf_file.read()
        self.vdf = '{' + self.replace_all_regex(self.vdf, replacements) + '}'
        self.json = json.loads(self.vdf)
        logging.info('finished loading .vdf into .json')

    def save_vdf(self) -> None:
        replacements = self.app.config.get('screenshot.metadata.regex_in')
        json_as_vdf = json.dumps(self.json, indent=4)
        json_as_vdf = self.replace_all_regex(json_as_vdf, replacements)
        path = self.app.config.get('screenshot.metadata.path')
        logging.info('open \'{}\''.format(path))
        with open(path, 'w') as vdf_file:
            vdf_file.write(json_as_vdf)
        logging.info('finished saving .json into .vdf')

    def replace_all_regex(self, target: str, replacements: list) -> str:
        for regex_pair in replacements:
            target[:] = re.sub(regex_pair[0], regex_pair[1], target)
        return target

    def add_screenshot(self, time: datetime.datetime, size: list) -> None:
        creation_seconds = int(time.timestamp())
        name_format = self.app.config.get('screenshot.')
        pass
