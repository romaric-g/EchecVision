import { Square } from "react-chessboard/dist/chessboard/types";

export type GameStatus = 'play' | 'pause' | 'none';

export interface GameLog {
    user: 'player' | 'ia',
    message: string,
    wait: boolean,
    time: number
}

export interface NewGameState {
    is_start: boolean,
    is_pause: boolean
}

export interface NewChessBoardState {
    "fen": string,
    "draw_moov": Square[]
}

export interface UpdateUrlData {
    url: string,
    url_connected: boolean,
    url_error: boolean
}



export interface InitalData {
    chess_board_state: any,
    game_logs: any[],
    is_pause: boolean,
    is_start: boolean,
    url: string,
    url_connected: boolean,
    url_error: boolean
  }