import classNames from "classnames";
import React from "react";
import { GameLog } from "../types";

interface Props {
    gameLog: GameLog
}

const GameStackItem : React.FC<Props> = (props) => {
    const {
        gameLog
    } = props;

    const icon = React.useMemo(() => {
        if (gameLog.user == 'ia') {
            return (
                <svg className="w-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M14.25 9.75L16.5 12l-2.25 2.25m-4.5 0L7.5 12l2.25-2.25M6 20.25h12A2.25 2.25 0 0020.25 18V6A2.25 2.25 0 0018 3.75H6A2.25 2.25 0 003.75 6v12A2.25 2.25 0 006 20.25z"></path>
                </svg>
            )
        }
        return (
            <svg className="w-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"></path>
            </svg>
        )
    }, [])

    return (
        <div className={classNames('p-4 flex flex-row gap-2', {
            'bg-white': gameLog.user == 'player'
        })}>
            <div className='flex items-center justify-center border border-slate-50 rounded-lg w-8 h-8 bg-white'>
                { icon }
            </div>
            <p>{gameLog.message}</p>
        </div>
    )


}

export default GameStackItem;