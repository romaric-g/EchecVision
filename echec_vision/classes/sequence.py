

class Sequence():

    objectif: int
    toletence: int

    is_finished: False
    valid_count: 0
    unvalid_count: 0

    def __init__(self, objectif, tolerence = 0) -> None:
        self.objectif = objectif
        self.toletence = tolerence

    def valid_next(self):
        self.valid_count = self.valid_count + 1

        if self.valid_count >= self.objectif:
            self.is_finished = True

    def unvalid_next(self):
        self.unvalid_count = self.unvalid_count + 1

        if self.toletence < self.unvalid_count:
            self.reset()

    def reset(self):
        self.is_finished = False
        self.valid_count = 0
        self.unvalid_count = 0