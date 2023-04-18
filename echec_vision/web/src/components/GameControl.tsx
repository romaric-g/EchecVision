import Button from "./Button"
import { AiFillSetting } from 'react-icons/ai'
import SettingsModal from "./SettingsModal"
import React from "react"
import { GlobalContext } from "../context/GlobalContext"
import StartControlButton from "./Controls/StartControlButton"
import { GameStatus } from "../types"
import StopControlButton from "./Controls/StopControlButton"

interface Props {
    status: GameStatus
}

const GameControl = (props: Props) => {
    const {
        status
    } = props

    const { socketInstance, setSocketInstance } = React.useContext(GlobalContext)
    const [isModal, setIsModal] = React.useState(false)

    console.log("socketInstance", socketInstance)
    console.log("status", status)

    return (
        <div className="actions flex p-4 gap-2">

            {status == 'none' && (
                <>
                    <StartControlButton />
                    <Button
                        className="flex-0"
                        icon={<AiFillSetting />}
                        type="second"
                        onClick={() => {
                            setIsModal(true)
                        }}
                    />

                </>
            )}

            {status == 'pause' && (
                <>
                    <Button
                        className="flex-1"
                        text="Reprendre"
                        type="second"
                        onClick={() => {

                        }}
                    />
                    <StopControlButton />
                </>
            )}

            {status == 'play' && (
                <>
                    <Button
                        className="flex-1"
                        text="Pause"
                        type="second"
                        onClick={() => {

                        }}
                    />
                    <StopControlButton />
                </>
            )}
            <SettingsModal
                closeModal={() => setIsModal(false)}
                showModal={isModal}
            />
        </div>
    )
}

export default GameControl