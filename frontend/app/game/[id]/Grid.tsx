"use client";
import React, { useEffect, useState } from "react";
import { observer } from "mobx-react-lite";
import { GridStoreProps } from "./GridStore";

import { faArrowDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

export interface GridProps {
	store: GridStoreProps;
	onClick: (col: number) => void;
}
export default observer(function Grid({ store, onClick }: GridProps) {
	function getCell(row: number, col: number) {
		let cell: JSX.Element;

		let colour: string = "bg-opacity-50 bg-grid-colour";

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

		if (isMyTurn && !store.game.endTime) {
			columnHighlight =
				col === store.columnHighlight ? "bg-[#B1DFE8] rounded-full" : "";

			if (columnState && store.columnHighlight === col) {
				columnHighlight = "";
			}
		}

		let border = "";

		const key = `${row}-${col}`;
		if (store.connectTokens.includes(key)) {
			border = "border-8 border-[#EAE151]";
		}

		cell = (
			<button
				key={`btn-${key}`}
				className={`m-auto flex h-24 w-24 ${columnHighlight} ${pointer}`}
				onMouseOver={() => {
					store.onMouseOver(col);
				}}
				onMouseOut={() => {
					store.onMouseOut(col);
				}}
				onClick={() => {
					onClick(col);
				}}
				disabled={columnState || !isMyTurn || store.game.endTime !== null}
			>
				<div
					key={`cell-${key}`}
					className={`${colour} ${border} m-auto flex h-20 w-20 rounded-full`}
				/>
			</button>
		);

		return cell;
	}

	function getRow(rowData: number[], rowIndex: number) {
		let row: JSX.Element;

		row = (
			<div
				key={`row-${rowIndex}`}
				className='flex flex-row justify-items-center gap-1'
			>
				{rowData.map((_, index) => {
					return getCell(rowIndex, index);
				})}
			</div>
		);

		return row;
	}

	function dropIndicator() {
		let row: JSX.Element;

		row = (
			<div className='flex h-8 w-full flex-row justify-items-center gap-1'>
				{store.game.board[0].map((_, index) => {
					const cols = store.game.board[0].length;
					const columnState = store.isColumnFull(index);

					let columnHighlight = "";
					if (store.isMyTurn()) {
						columnHighlight =
							index === store.columnHighlight ? "block" : "hidden";

						if (columnState && store.columnHighlight === index) {
							columnHighlight = "hidden";
						}
					}

					return (
						<div key={`col-${index}`} className='flex h-full w-full'>
							<FontAwesomeIcon
								key={`drop-${index}`}
								icon={faArrowDown}
								size='xl'
								className={`${columnHighlight} fa-bounce m-auto`}
							/>
						</div>
					);
				})}
			</div>
		);

		return row;
	}

	return (
		<div className='m-auto flex w-full pt-[3rem]'>
			<div className='m-auto h-fit w-fit'>
				<div className='flex flex-col justify-items-center gap-1'>
					{dropIndicator()}
					{store.game.board.map((rowData, index) => {
						return getRow(rowData, index);
					})}
				</div>
			</div>
		</div>
	);
});
