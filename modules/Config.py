import os
import json
import inspect
import logging
import shared.modulebase


class Config(shared.modulebase.ModuleBase):

    def preferred_load_index(self) -> int:
        return 1

    def on_load(self) -> None:
        self.path = os.path.abspath('data/config.json')
        with open(self.path, 'r') as config_file:
            self.data = json.load(config_file)
        self.prepare_variables()
        self.recursive_replace_variables(self.data)

    def prepare_variables(self) -> None:
        self.variables = {}
        for key in self.data['variables']:
            self.variables[key] = os.path.expandvars(
                self.data['variables'][key]
            )
        del(self.data['variables'])

    def recursive_replace_variables(self, data: dict) -> None:
        for key in data:
            if key == 'variables':
                continue
            elif type(data[key]) is str:
                data[key] = os.path.expandvars(
                    data[key].format(**self.variables)
                )
            elif type(data[key]) is dict:
                self.recursive_replace_variables(data[key])

    def get(self, key) -> any:
        split_key = key.split('.')
        value = self.data
        for k in split_key:
            value = value[k]
        return value
