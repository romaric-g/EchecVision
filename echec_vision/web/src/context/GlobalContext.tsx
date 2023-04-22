import React from 'react';
import { GameLog } from '../types';
import { Socket } from 'socket.io-client';

interface Provider {
    logs?: GameLog[]
    setLogs?: React.Dispatch<React.SetStateAction<GameLog[]>>
    url?: string
    setUrl?: React.Dispatch<React.SetStateAction<string>>
    stockfishPath?: string,
    setStockfishPath?: React.Dispatch<React.SetStateAction<string>>
    socketInstance?: Socket
    setSocketInstance?: (socket: Socket) => void
    isStart?: boolean,
    setIsStart?: React.Dispatch<React.SetStateAction<boolean>>
    isPause?: boolean,
    setIsPause?: React.Dispatch<React.SetStateAction<boolean>>

}

interface Props {
    children: JSX.Element
}

export const GlobalContext = React.createContext<Provider>({});

export const GlobalProvider = (props: Props) => {
    const [logs, setLogs] = React.useState<GameLog[]>([])
    const [url, setUrl] = React.useState("")
    const [stockfishPath, setStockfishPath] = React.useState("")
    const [isStart, setIsStart] = React.useState(false)
    const [isPause, setIsPause] = React.useState(false)
    const [socketInstance, setSocketInstance] = React.useState<Socket>();

    return (
        <GlobalContext.Provider
            value={{
                logs,
                setLogs,
                url,
                setUrl,
                stockfishPath,
                setStockfishPath,
                socketInstance,
                setSocketInstance,
                isStart,
                setIsStart,
                isPause,
                setIsPause
            }}
        >
            {props.children}
        </GlobalContext.Provider>
    )
}