import React from 'react';
import { GameLog } from '../types';
import { Socket } from 'socket.io-client';

interface Provider {
    logs?: GameLog[],
    setLogs?: (gameLogs: GameLog[]) => void,
    url?: string,
    setUrl?: (url: string) => void,
    socketInstance?: Socket,
    setSocketInstance?: (socket: Socket) => void;
}

interface Props {
    children: JSX.Element
}

export const GlobalContext = React.createContext<Provider>({});

export const GlobalProvider = (props: Props) => {
    const [logs, setLogs] = React.useState<GameLog[]>([])
    const [url, setUrl] = React.useState("")
    const [socketInstance, setSocketInstance] = React.useState<Socket>();

    return (
        <GlobalContext.Provider
            value={{
                logs,
                setLogs,
                url,
                setUrl,
                socketInstance,
                setSocketInstance
            }}
        >
            {props.children}
        </GlobalContext.Provider>
    )
}