from dataclasses import dataclass


@dataclass
class Symbol:
    def __init__(self, name: str, full_name=''):
        self.name = name
        self.full_name = full_name
