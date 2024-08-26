import React from "react";
import Grid from "./Grid";
import Banner from "@/components/Banner";
import Link from "next/link";
import Timer from "./components/Timer";

import { getGameData } from "@/actions/getGameData";

interface GameProps {
  params: {
    id: string;
  };
}

async function Game({ params: { id } }: GameProps) {
  const game = await getGameData(id);

  let startDate = null;
  let endDate = null;

  if (game) {
    if (game.startTime) {
      startDate = new Date(game.startTime);
    }
    if (game.endTime) {
      endDate = new Date(game.endTime);
    }
  }

  return (
    <div className="grid h-screen grid-cols-2 gap-8">
      <div>
        <div className="m-auto flex h-[90vh] w-full">
          <div className="m-auto flex h-full w-full flex-col rounded-2xl bg-bgc pl-9 pr-9">
            <div className="h-1/4 w-full flex-col text-balance pb-52 pt-14 text-left font-sans text-5xl leading-normal text-black">
              <Timer startDate={startDate} endDate={endDate} />
            </div>
            <div className="m-auto flex h-3/4 w-full flex-col"></div>
          </div>
        </div>
      </div>
      <div className="gridRight">
        <h3 className="flex justify-center font-sans text-2xl font-medium leading-loose">
          Drop your token on your turn
        </h3>
        <Grid gameId={id} />
        <div className="relative h-[5rem]">
          <div className="insert-x-0 absolute bottom-0 w-[40rem]">
            <div>
              <Link
                className="flex flex-row justify-center pt-2 font-medium text-slate-400"
                href="/"
              >
                Resign
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Game;
