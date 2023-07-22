import React from 'react';
import { GlobalContext } from "../../context/GlobalContext";
import Button from "../Button";

const PauseControlButton: React.FC = () => {

    const { socketInstance, setSocketInstance } = React.useContext(GlobalContext)

    const [isLoading, setIsLoading] = React.useState(false);

    const handleStart = React.useCallback(() => {
        setIsLoading(true)

        socketInstance?.emit("resume")

    }, [isLoading, setIsLoading])

    return (
        <Button
            className="flex-1"
            text="Reprendre"
            type="second"
            isLoading={isLoading}
            onClick={handleStart}
        />
    )
}
export default PauseControlButton;