from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Symbol:
    def __init__(self, name: str, full_name=''):
        self.name = name
        self.full_name = full_name
