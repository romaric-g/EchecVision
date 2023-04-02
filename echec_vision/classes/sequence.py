

class Sequence():

    toletence: int

    valid_count: 0
    unvalid_count: 0

    def __init__(self, tolerence=0) -> None:
        self.toletence = tolerence

    def valid_next(self):
        self.valid_count = self.valid_count + 1

    def unvalid_next(self):
        self.unvalid_count = self.unvalid_count + 1

        if self.toletence < self.unvalid_count:
            self.valid_count = 0
            self.unvalid_count = 0
