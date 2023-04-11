import Button from "./Button"
import { AiFillSetting } from 'react-icons/ai'
import SettingsModal from "./SettingsModal"
import React from "react"

interface Props {
    status: 'play' | 'pause' | 'none'
}

const GameControl = (props: Props) => {
    const {
        status
    } = props

    const [isModal, setIsModal] = React.useState(false)

    const buttons = null

    return (
        <div className="actions flex p-4 gap-2">

            {status == 'none' && (
                <>
                    <Button
                        className="flex-1"
                        text="Commencer"
                        type="success"
                        onClick={() => {

                        }}
                    />
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
                    <Button
                        className="flex-1"
                        text="Arreter"
                        type="danger"
                        onClick={() => {

                        }}
                    />
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
                    <Button
                        className="flex-1"
                        text="Arreter"
                        type="danger"
                        onClick={() => {

                        }}
                    />
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