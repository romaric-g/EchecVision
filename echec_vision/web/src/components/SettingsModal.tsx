import React from "react";
import Input from "./Input";
import Button from "./Button";
import { GlobalContext } from "../context/GlobalContext";

interface Props {
    showModal: boolean,
    closeModal: () => void
}

const SettingsModal = (props: Props) => {
    const {
        showModal,
        closeModal
    } = props

    const [tempUrl, setTempUrl] = React.useState("")
    const [tempStockfishPath, setTempStockfishPath] = React.useState("")

    const { url, stockfishPath, setUrl, setStockfishPath, socketInstance } = React.useContext(GlobalContext);


    const handleCancel = React.useCallback(() => {
        setTempUrl(url || "")
        setTempStockfishPath(stockfishPath || "")
        closeModal()
    }, [url, stockfishPath])


    const handleSave = React.useCallback(() => {
        console.log("socketInstance", socketInstance)
        if (socketInstance) {
            socketInstance.emit("settings", { url: tempUrl, stockfish_path: tempStockfishPath })
        }
        if (setUrl) {
            setUrl(tempUrl)
        }
        if (setStockfishPath) {
            setStockfishPath(tempStockfishPath)
        }
        closeModal()
    }, [socketInstance, tempUrl, tempStockfishPath, setUrl, setStockfishPath, closeModal])


    React.useEffect(() => {
        if (url) {
            setTempUrl(url)
        } else {
            setTempUrl("")
        }
    }, [url])

    React.useEffect(() => {
        if (stockfishPath) {
            setTempStockfishPath(stockfishPath)
        } else {
            setTempStockfishPath("")
        }
    }, [stockfishPath])

    return (
        <>
            {showModal && (
                <>
                    <div
                        className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none"
                    >
                        <div className="relative w-auto my-6 mx-auto max-w-3xl">
                            {/*content*/}
                            <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                                {/*header*/}
                                <div className="flex items-start justify-between p-5 border-b border-solid border-slate-200 rounded-t">
                                    <h3 className="text-3xl font-semibold">
                                        Paramètres
                                    </h3>
                                    <button
                                        className="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                                        onClick={handleCancel}
                                    >
                                        <span className="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none">
                                            ×
                                        </span>
                                    </button>
                                </div>
                                {/*body*/}
                                <div className="relative p-6 flex-auto">
                                    <div className="w-96">
                                        <Input
                                            text={tempUrl}
                                            setText={setTempUrl}
                                            placeholder="URL de la camera"
                                        />
                                        <Input
                                            text={tempStockfishPath}
                                            setText={setTempStockfishPath}
                                            placeholder="Chemin d'acces à stockfish.exe"
                                        />
                                    </div>
                                </div>
                                {/*footer*/}
                                <div className="flex items-center justify-end p-6 border-t border-solid border-slate-200 rounded-b">
                                    <Button
                                        onClick={() => handleCancel()}
                                        className="ml-2"
                                        text="Annuler"
                                        type="danger"
                                    />
                                    <Button
                                        onClick={() => handleSave()}
                                        className="ml-2"
                                        text="Sauvegarder"
                                        type="success"
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className="opacity-25 fixed inset-0 z-40 bg-black"></div>
                </>
            )}
        </>
    );
}

export default SettingsModal