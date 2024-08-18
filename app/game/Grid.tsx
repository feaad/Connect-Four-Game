"use client";
import React from "react";
import { observer, useLocalObservable } from "mobx-react-lite";
import GridStore from "./GridStore";

export default observer(function Grid() {
  // const chipColor = "bg-grid-colour";

  const store = useLocalObservable(() => GridStore);

  const data = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
  ];

  store.init(data);

  function getCell(row: number, col: number) {
    let cell: JSX.Element;

    let colour: string = "bg-grid-colour";

    const columnState = store.isColumnFull(col);
    const pointer = columnState ? "cursor-not-allowed" : "";

    const token = store.getToken(row, col);

    if (token === 1) {
      colour = "bg-player1";
    } else if (token === 2) {
      colour = "bg-player2";
    }

    let columnHighlight =
      col === store.columnHighlight ? "bg-[#B1DFE8] rounded-full" : "";

    if (columnState && store.columnHighlight === col) {
      columnHighlight = "";
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
          store.onCellClick(col);
        }}
        disabled={columnState}
      >
        <div className={`${colour} m-auto flex h-16 w-16 shadow-inner shadow-gray-700 rounded-full `} />
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
    <div className="m-auto flex h-full w-full">
      <div className="m-auto h-fit w-fit">
        <div className="flex flex-col justify-items-center gap-1">
          {store.data.map((rowData, index) => {
            return getRow(rowData, index);
          })}
        </div>
      </div>
    </div>
  );
});
