import React from 'react'
import { Chessboard } from "react-chessboard"
import { io, Socket } from "socket.io-client";
import GameStackItem from './components/GameStackItem'
import { GameLog, GameStatus, InitalData, NewChessBoardState, NewGameState } from './types';
import GameControl from './components/GameControl';
import SettingsModal from './components/SettingsModal';
import { GlobalContext, GlobalProvider } from './context/GlobalContext';
import StatusBar from './components/StatusBar';
import LogStack from './components/LogStack';
import { Square } from 'react-chessboard/dist/chessboard/types';

const PORT = 5000

const App = () => {
  const [initalData, setInitalData] = React.useState<InitalData>()
  const [fen, setFen] = React.useState<string>()
  const [drawMove, setDrawMove] = React.useState<Square[]>()

  const { socketInstance, logs, isStart, isPause, setSocketInstance, setUrl, setStockfishPath, setLogs, setIsPause, setIsStart } = React.useContext(GlobalContext)

  const loadInitalData = React.useCallback(async () => {
    const response = await fetch("http://localhost:" + PORT + "/init")
    const json = await response.json()

    if (json) {
      const initalData: InitalData = json;

      setInitalData(initalData)

      setUrl!(initalData.url)
      setStockfishPath!(initalData.stockfish_path)
      setLogs!(initalData.game_logs.map((gl) => {
        return {
          message: gl.message,
          time: gl.time,
          user: gl.user,
          wait: gl.wait
        };
      }))

      setIsStart!(initalData.is_start)
      setIsPause!(initalData.is_pause)
    }

  }, [setIsStart, setIsPause])

  React.useEffect(() => {
    console.log("setSocketInstance", setSocketInstance)
    if (!setSocketInstance) return;

    console.log("START")
    const socket = io("http://localhost:" + PORT + "/");

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

    socket.on("new_game_state", (newGameState: NewGameState) => {
      console.log("newGameState", newGameState)

      setIsStart!(newGameState.is_start)
      setIsPause!(newGameState.is_pause)

    })

    socket.on("new_chess_board_state", (data: any) => {

      let newChessBoardState: NewChessBoardState = JSON.parse(data);
      console.log("newChessBoardState", newChessBoardState)
      console.log("new fen", newChessBoardState.fen)
      console.log("new draw_move", newChessBoardState.draw_moov)
      setFen(newChessBoardState.fen)
      setDrawMove(newChessBoardState.draw_moov)
    })

    loadInitalData()

    return () => {
      console.log("END")
      socket.disconnect();
    };
  }, [setSocketInstance, loadInitalData, setIsStart, setIsPause]);

  const status: GameStatus = React.useMemo<GameStatus>(() => {
    if (isStart) {
      if (isPause) {
        return 'pause'
      } else {
        return 'play'
      }
    }
    return 'none'
  }, [isStart, isPause])

  const reset = React.useCallback(async () => {
    const response = await fetch("http://localhost:" + PORT + "/init")
    const json = await response.json()

    if (json) {
      const initalData: InitalData = json;

      setInitalData(initalData)

      setUrl!(initalData.url)
      setStockfishPath!(initalData.stockfish_path)
      setLogs!(initalData.game_logs.map((gl) => {
        return {
          message: gl.message,
          time: gl.time,
          user: gl.user,
          wait: gl.wait
        };
      }))
    }
  }, [setSocketInstance, loadInitalData, setIsStart, setIsPause])

  const pushLog = React.useCallback((gameLog: GameLog) => {
    setLogs!((prevLogs) => [...prevLogs, gameLog])
  }, [setLogs])


  React.useEffect(() => {
    if (isStart) {
      reset()
    }
  }, [isStart, reset, setInitalData])

  if (!initalData) {
    return <div className="h-screen w-screen flex items-center justify-center bg-slate-900 text-white">
      <div className='flex flex-col items-center gap-4'>
        <p className="font-medium">Echec vision</p>
        <div role="status">
          <svg aria-hidden="true" className="inline w-10 h-10 mr-2 text-gray-200 animate-spin dark:text-white fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor" />
            <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill" />
          </svg>
          <span className="sr-only">Loading...</span>
        </div>
      </div>
    </div >
  }

  console.log("fen", fen)
  console.log("drawMove", drawMove)


  return (
    <div className="flex h-screen">
      <div className="flex-1 bg-black flex justify-center items-center p-10 ">

        <div className="w-full lg:w-2/3 rounded-xl overflow-hidden">
          <Chessboard
            id="BasicBoard"
            customArrows={drawMove ? [drawMove] : []}
            areArrowsAllowed={false}
            arePremovesAllowed={false}
            arePiecesDraggable={false}
            position={fen}
          />
        </div>

      </div>
      <div className="w-96 flex-initial flex flex-col">
        <StatusBar initalData={initalData} />
        <LogStack logs={logs || []} />
        <GameControl status={status} />
      </div>
    </div>
  )
}

export default App
