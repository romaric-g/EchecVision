import React from 'react'
import { Chessboard } from "react-chessboard"
import { io, Socket } from "socket.io-client";
import GameStackItem from './components/GameStackItem'
import { GameLog } from './types';
import GameControl from './components/GameControl';
import SettingsModal from './components/SettingsModal';
import { GlobalContext, GlobalProvider } from './context/GlobalContext';


const App = () => {
  const [gameLogs, setGameLogs] = React.useState<GameLog[]>([])

  const { socketInstance, setSocketInstance } = React.useContext(GlobalContext)

  React.useEffect(() => {
    console.log("setSocketInstance", setSocketInstance)
    if (!setSocketInstance) return;

    console.log("START")
    const socket = io("http://localhost:5001/");

    console.log("new socket", socket)
    setSocketInstance(socket);

    socket.on("connect", () => {
      console.log("connect");
    });

    socket.on("disconnect", (data) => {
      console.log("disconnect")
      console.log(data);
    });

    socket.on("new_game_log", (e) => {

      let data = JSON.parse(e);
      console.log("new game", e)
      console.log("a", data)

      pushLog({
        user: data["user"],
        message: data["message"],
        time: data["time"],
        wait: data["wait"]
      })
    })

    socket.on('data', (e) => {
      console.log("data", e)
    })

    return () => {
      console.log("END")
      socket.disconnect();
    };
  }, [setSocketInstance]);

  console.log("B", socketInstance)
  console.log(gameLogs)

  const pushLog = React.useCallback((gameLog: GameLog) => {
    setGameLogs(prevGameLogs => [...prevGameLogs, gameLog])
  }, [setGameLogs])

  const onHandleClick = React.useCallback(() => {
    console.log("Click")
    // console.log(socketInstance)
    socketInstance?.emit("data", { "test": 'ezeqz' })
  }, [socketInstance])

  return (
    <div className="flex h-screen">
      <div className="flex-1 bg-black flex justify-center items-center p-10 ">

        <div className="w-full lg:w-2/3 rounded-xl overflow-hidden">
          <Chessboard
            id="BasicBoard"
            customArrows={[['a3', 'a5'], ['g1', 'f3']]}
            areArrowsAllowed={false}
            arePremovesAllowed={false}
            arePiecesDraggable={false}
          />
        </div>

      </div>
      <div className="w-96 flex-initial flex flex-col">
        <div className="status p-4 bg-green-400">
          <p className='text-white'>Actuellement connecté à 10.126.43.10:3000</p>
        </div>
        <div className="stack grow bg-gray-200">
          {gameLogs.map((gameLog) => (
            <GameStackItem gameLog={gameLog} />
          ))}
        </div>
        <GameControl status='none' />
      </div>
    </div>
  )
}

export default App
