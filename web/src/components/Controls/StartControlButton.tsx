import React from 'react';
import { GlobalContext } from "../../context/GlobalContext";
import Button from "../Button";

interface Props {

}

const StartControlButton: React.FC<Props> = (props) => {

    const { } = props
    const { socketInstance, setSocketInstance } = React.useContext(GlobalContext)

    const [isLoading, setIsLoading] = React.useState(false);

    const handleStart = React.useCallback(() => {
        setIsLoading(true)

        socketInstance?.emit("start")

    }, [isLoading, setIsLoading])

    return (
        <Button
            className="flex-1"
            text="Commencer"
            type="success"
            isLoading={isLoading}
            onClick={handleStart}
        />
    )
}
export default StartControlButton;