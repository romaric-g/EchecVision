import time


class GameLog(dict):

    def __init__(self, user='player', message=None, wait=False) -> None:
        dict.__init__(self, user=user, message=message,
                      wait=wait, time=time.time())


    