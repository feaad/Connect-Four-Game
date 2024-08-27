"use client";
import React, { useEffect, useState } from "react";
import useWebSocket, { UseWebSocketProps } from "@/hooks/useWebSocket";
import { observer, useLocalObservable } from "mobx-react-lite";
import GridStore from "./GridStore";

export interface GridProps {
  gameId: string;
}
export default observer(function Grid({ gameId }: GridProps) {
  const store = useLocalObservable(() => GridStore);
  const [connect, setConnect] = useState<boolean>(true);

  const [webSocketConfig, setWebSocketConfig] =
    useState<UseWebSocketProps | null>(null);

  const { sendMessage, receivedMessage, connectionStatus } = useWebSocket({
    path: "/game/" + gameId,
  });

  store.init(gameId);


  useEffect(() => {
    if (connectionStatus === 1 && !connect) {
      setConnect(true);
      store.setLoading(false);
    }

    if (connectionStatus === 3) {
      setConnect(false);
      store.setLoading(true);
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
    if (!store.isMyTurn()) {
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

  function getCell(row: number, col: number) {
    let cell: JSX.Element;

    let colour: string = "bg-grid-colour";

    const columnState = store.isColumnFull(col);
    const isMyTurn = store.isMyTurn();
    const pointer = columnState || !isMyTurn ? "cursor-not-allowed" : "";

    const token = store.getToken(row, col);

    if (token === 1) {
      colour = "bg-player1";
    } else if (token === 2) {
      colour = "bg-player2";
    }
    let columnHighlight = "";

    if (isMyTurn) {
      columnHighlight =
        col === store.columnHighlight ? "bg-[#B1DFE8] rounded-full" : "";

      if (columnState && store.columnHighlight === col) {
        columnHighlight = "";
      }
    }

    // TODO: Make this Visually Pleasing
    let border = "";

    const key = `${row}-${col}`;
    if (store.connectTokens.includes(key)) {
      border = "border-4 border-blue-500";
    }

    cell = (
      <button
        className={`m-auto flex h-20 w-20 ${columnHighlight} ${pointer}`}
        onMouseOver={() => {
          store.onMouseOver(col);
        }}
        onMouseOut={() => {
          store.onMouseOut(col);
        }}
        onClick={() => {
          handleOnClick(col);
        }}
        disabled={columnState || !isMyTurn}
      >
        <div
          className={`${colour} ${border} m-auto flex h-16 w-16 rounded-full shadow-inner shadow-gray-700`}
        />
      </button>
    );

    return cell;
  }

  function getRow(rowData: number[], rowIndex: number) {
    let row: JSX.Element;

    row = (
      <div className="flex flex-row justify-items-center gap-1">
        {rowData.map((_, index) => {
          return getCell(rowIndex, index);
        })}
      </div>
    );

    return row;
  }

  return (
    <>
      {store.loading ? (
        // TODO: Making your loading screen look better
        <div className="flex h-full w-full">
          <span className="loading loading-dots loading-lg m-auto"></span>
        </div>
      ) : (
        <div className="m-auto flex w-full pt-[5rem]">
          <div className="m-auto h-fit w-fit">
            <div className="flex flex-col justify-items-center gap-1">
              {store.game.board.map((rowData, index) => {
                return getRow(rowData, index);
              })}
            </div>
          </div>
        </div>
      )}
    </>
  );
});
