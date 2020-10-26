import os
import datetime
from luaparser import ast, astnodes


class Member(object):

    username: str
    rank: str
    note: str
    online: datetime.datetime

    def __init__(self, username: str, rank: str, online: str, note: str = None) -> None:
        super().__init__()
        self.username = username
        self.rank = rank
        self.online = datetime.datetime.strptime(online, '%Y-%m-%d %H:%M:%S')
        self.note = note

    def tostring(self, separator: str = ';') -> str:
        return separator.join([
            self.username,
            self.rank,
            self.online.strftime('%Y-%m-%d %H:%M:%S'),
            self.note if self.note else ''
        ])

    @classmethod
    def headers(self, separator: str = ';') -> str:
        return separator.join([
            'Username',
            'Rank',
            'Online',
            'Note'
        ])


class Trinket(object):

    luatree: astnodes.Node = None
    memberdata: list = list()

    def load(self, luapath: str) -> None:
        print(f'Load Lua: {luapath}')
        with open(luapath, 'r', encoding='utf-8') as infile:
            luastring: str = infile.read()
            self.luatree = ast.parse(luastring)

    def process_field(self, field: astnodes.Field) -> None:
        self.memberdata.append(Member(
            # note=field.value.fields[0].value.s,
            rank=field.value.fields[3].value.s,
            username=field.value.fields[2].value.s,
            online=field.value.fields[1].value.s
        ))

    def process(self) -> None:
        total_processed: int = 0
        for node in ast.walk(self.luatree):
            if isinstance(node, astnodes.Field) and hasattr(field.key, 'n'):
                self.process_field(node)
                total_processed += 1
        print(f'Processed total {total_processed} nodes')

    def write_csv(self, csvpath: str, separator: str = ';') -> None:
        print(f'Write CSV -> {csvpath}')
        with open(csvpath, 'w', encoding='utf-8') as outfile:
            outfile.write(f'{Member.headers(separator)}\n')
            for member in sorted(self.memberdata, key=lambda k: k.username):
                outfile.write(f'{member.tostring(separator)}\n')


if __name__ == '__main__':
    luapath = os.path.join(
        os.path.expandvars('%UserProfile%'), 'Documents', 'Elder Scrolls Online',
        'live', 'SavedVariables', 'Trinket.lua'
    )
    csvpath = os.path.join(os.path.dirname(__file__), 'Trinket.csv')
    parser = Trinket()
    parser.load(luapath)
    parser.process()
    parser.write_csv(csvpath)
