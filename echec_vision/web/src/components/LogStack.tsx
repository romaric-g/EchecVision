import { GameLog } from "../types";
import GameStackItem from "./GameStackItem";

interface Props {
    logs: GameLog[]
}

const LogStack: React.FC<Props> = (props) => {
    const {
        logs
    } = props

    return (
        <div className="stack grow bg-gray-200">
            {logs!.map((log) => (
                <GameStackItem gameLog={log} />
            ))}
        </div>
    )
}

export default LogStack;