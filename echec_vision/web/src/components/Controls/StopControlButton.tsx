import React from 'react';
import { GlobalContext } from "../../context/GlobalContext";
import Button from "../Button";

interface Props {
}

const StopControlButton: React.FC<Props> = (props) => {

    const { } = props
    const { socketInstance, setIsStart, setIsPause } = React.useContext(GlobalContext)

    const handleStopGame = React.useCallback(() => {
        console.log("handleStopGame")
        socketInstance?.emit("stop")

        console.log("stop : socketInstance", socketInstance)

        setIsStart!(false)
        setIsPause!(false)
    }, [socketInstance, setIsStart, setIsPause])

    return (
        <Button
            className="flex-1"
            text="Arreter"
            type="danger"
            onClick={handleStopGame}
        />
    )
}
export default StopControlButton;