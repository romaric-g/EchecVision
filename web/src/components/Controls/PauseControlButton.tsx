import React from 'react';
import { GlobalContext } from "../../context/GlobalContext";
import Button from "../Button";

const PauseControlButton: React.FC = () => {

    const { socketInstance, setSocketInstance } = React.useContext(GlobalContext)

    const [isLoading, setIsLoading] = React.useState(false);

    const handleStart = React.useCallback(() => {
        setIsLoading(true)

        socketInstance?.emit("pause")

    }, [isLoading, setIsLoading])

    return (
        <Button
            className="flex-1"
            text="Pause"
            type="second"
            isLoading={isLoading}
            onClick={handleStart}
        />
    )
}
export default PauseControlButton;