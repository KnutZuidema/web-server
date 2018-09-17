from typing import Generator


class ReturnValueGenerator:
    def __init__(self, gen: Generator):
        self.gen = gen

    def __iter__(self):
        self.value = yield from self.gen
