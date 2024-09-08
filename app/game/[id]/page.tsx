import { Game as GameType } from "@/types/types";
import { getGameData } from "@/actions/getGameData";
import { revalidatePath } from "next/cache";

import Game from "./Game";

export const revalidate = 0;
interface GameProps {
  params: {
    id: string;
  };
}

async function GamePage({ params: { id } }: GameProps) {
  revalidatePath("/game/" + id, "page");
  const game = (await getGameData(id)) as GameType;

  if (!game) {
    return (
      <div className="m-auto flex h-full w-full bg-red-600">
        <div className="text-mono m-auto flex h-full w-full text-6xl text-white">
          Game Not Found
        </div>
      </div>
    );
  }

  return <Game gameData={game} />;
}

export default GamePage;
