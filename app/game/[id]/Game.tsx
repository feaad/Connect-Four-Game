"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Grid from "./Grid";
import Link from "next/link";
import Timer from "./components/Timer";

import { Game as GameType } from "@/types/types";

import GridStore from "./GridStore";
import { observer, useLocalObservable } from "mobx-react-lite";
import useWebSocket, { UseWebSocketProps } from "@/hooks/useWebSocket";
import Waiting from "@/app/sharelink/[id]/Waiting";
import WaitScreen from "@/components/WaitScreen";
import { getToken } from "next-auth/jwt";

interface GameProps {
  gameData: GameType;
}

export default observer(function Game({ gameData }: GameProps) {
  const router = useRouter();
  const store = useLocalObservable(() => GridStore);

  const [webSocketConfig, setWebSocketConfig] =
    useState<UseWebSocketProps | null>(null);

  const { sendMessage, receivedMessage, connectionStatus } = useWebSocket({
    path: "/game/" + gameData.gameId,
  });
  const [initialized, setInitialized] = useState(false);

  store.init(gameData);

  useEffect(() => {
    if (connectionStatus != 1 && initialized) {
      store.setGameData();
    } else if (connectionStatus == 1 && !initialized) {
      setInitialized(true);
    }
  }, [connectionStatus]);

  useEffect(() => {
    if (receivedMessage) {
      const message = JSON.parse(receivedMessage);
      if (message.event_type && message.event_type === "player_move") {
        const player = message.player_token;

        if (player === store.token) {
          return;
        }

        const { row, column } = message.message;
        store.updateGame(player, row, column);
      } else if (message.message && message.message.player) {
        const { player, row, column } = message.message;

        if (player === store.token) {
          return;
        }
        store.updateGame(player, row, column);
      } else if (message.message && message.message.status) {
        store.setStatus(message.message.status);
        store.setAllConnected();
      }
    }
  }, [receivedMessage]);

  function handleOnClick(col: number) {
    if (!store.isMyTurn() || store.game.endTime) {
      // TODO: Show a message to the user that it's not their turn
      return;
    }

    const message = {
      type: "player_move",
      column: col,
      row: store.emptyRows[col],
    };
    sendMessage(JSON.stringify(message));
    store.onCellClick(col);
  }

  function handleResult() {
    let results = "";
    if (
      store.connectTokens.length > 0 &&
      store.connectTokens.includes(store.token.toString())
    ) {
      results = store.game.username + " won!";
    } else if (
      store.connectTokens.length > 0 &&
      !store.connectTokens.includes(store.token.toString())
    ) {
      results = store.token == 1 ? store.game.playerTwo : store.game.playerOne;
      results += " won!";
    } else {
      results = "It's a draw!";
    }
    return results;
  }

  return (
    <div className="-m-11 h-screen w-screen bg-btn-colour">
      {store.loading || connectionStatus != 1 || !initialized ? (
        <WaitScreen title={"Game Loading"} />
      ) : (
        <div>
          <div className="grid grid-cols-3 gap-8 p-12">
            <div className="h-[90vh]">
              <Timer store={store} />
              <div className="w-120 flex justify-center pt-20">
                <div className="bg-2D565B bg-grid-bg card w-full">
                  <div className="card-body">
                    <h2 className="font-sans text-white text-3xl">{`It is ${store.game.currentTurn}'s turn`}</h2>
                   
                  </div>
                </div>
              </div>
              <div className="pt-20">
                <div className="bg-2D565B bg-grid-bg card w-full">
                  <div className="card-body">
                    <h2 className="font-sans text-[#FF922D]">How to play</h2>
                    <p className="font-sans text-white">
                      Drop your token on your turn. Win the game by connecting
                      four of your tokens diagonally, horizontally or
                      vertically.
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div className="bg-grid-bg col-span-2 rounded-[14px]">
              {store.game.endTime && (
                <div className="flex justify-center pt-10 text-5xl text-white">
                  {handleResult()}
                </div>
              )}
              <Grid store={store} onClick={handleOnClick} />
            </div>
          </div>
        </div>
        // <div className="grid h-screen grid-cols-2 gap-8">
        //   <div>
        //     <div className="m-auto flex h-[90vh] w-full">
        //       <div className="m-auto flex h-full w-full flex-col rounded-2xl bg-bgc pl-9 pr-9">
        //         <div className="h-1/4 w-full flex-col text-balance pb-52 pt-14 text-left font-sans text-5xl leading-normal text-black">
        //           <Timer store={store} />
        //         </div>
        //         <div className="m-auto flex h-3/4 w-full flex-col"></div>
        //       </div>
        //     </div>
        //   </div>
        //   <div className="gridRight">
        //     <h3 className="flex justify-center font-sans text-2xl font-medium leading-loose">
        //       Drop your token on your turn
        //     </h3>
        //     <Grid store={store} onClick={handleOnClick} />
        //     <div className="relative h-[5rem]">
        //       <div className="insert-x-0 absolute bottom-0 w-[40rem]">
        //         <div>
        //           <Link
        //             className="flex flex-row justify-center pt-2 font-medium text-slate-400"
        //             href="/"
        //           >
        //             Resign
        //           </Link>
        //         </div>
        //       </div>
        //     </div>
        //   </div>
        // </div>
      )}
    </div>
  );
});
