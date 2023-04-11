
export interface GameLog {
    user: 'player' | 'ia',
    message: string,
    wait: boolean,
    time: number
}
