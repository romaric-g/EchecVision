import time

class GameLog(dict):

    def __init__(self, user='player', message=None, wait=False) -> None:
        dict.__init__(self, user=user, message=message,
                      wait=wait, time=time.time())


class ChessBoardState(dict):

    def __init__(self, fen, draw_moov = None) -> None:
        dict.__init__(self, fen=fen, draw_moov=draw_moov, time=time.time())