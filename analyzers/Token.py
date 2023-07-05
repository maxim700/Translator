import rply


class Token(rply.Token):
    __match_args__ = ('name', 'value')
    

    def __init__(self, name, value, source_pos=None):
        super().__init__(name, value, source_pos)

    def __str__(self) -> str:
        return f'({self.name}; {self.value})'

    def __repr__(self):
        return str(self)