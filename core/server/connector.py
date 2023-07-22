from core.server.types import GameLog, ChessBoardState
from flask_socketio import SocketIO, emit
import chess
import json

# ------------------------------------------------------------
# Permet de faire le lien entre le programme et le client web
# ------------------------------------------------------------


class Connector:

    chess_board_state_dumps = None
    game_logs_dumps = []

    def update_game_state(self):
        self.get_socketio().emit("new_game_state", {
            'is_pause': self.get_session().is_pause,
            'is_start': self.get_session().is_start
        })

    def update_url_data(self):
        self.get_socketio().emit("update_url_data", {
            'url': self.get_session().url,
            'url_connected': self.get_session().url_connected,
            'url_error': self.get_session().url_error
        })

    # Permet d'effacer la liste des logs de partie et de les effacer sur le client web
    def clear_game_log(self):
        self.game_logs = []
        self.get_socketio().emit("clear_game_logs", json.dumps({}))

    # Permet d'enregister un nouveau log de jeu et de l'envoyer au client web
    def push_game_log(self, game_log: GameLog):
        game_log_dumbs = json.dumps(game_log)
        self.game_logs_dumps.append(game_log_dumbs)

        self.get_socketio().emit("new_game_log", game_log_dumbs)

    # Permet de mettre à jour l'êtat du plateau affiché sur le client web
    def update_chess_board_state(self, draw_moov=None):

        session = self.get_session()

        print("draw_moov", draw_moov)

        draw_moov_parse = None

        if draw_moov is not None:
            draw_moov_parse = [chess.square_name(
                draw_moov.from_square), chess.square_name(draw_moov.to_square)]

        if session is not None and session.is_start:
            chess_board_state: ChessBoardState = ChessBoardState(
                fen=session.move_detector.game.board.fen(),
                draw_moov=draw_moov_parse
            )

            self.chess_board_state_dumps = json.dumps(chess_board_state)
            self.get_socketio().emit("new_chess_board_state", self.chess_board_state_dumps)

    def get_session(self):
        from core.session import session
        return session

    def get_socketio(self) -> SocketIO:
        from core.server.server import socketio
        return socketio


connector = Connector()
