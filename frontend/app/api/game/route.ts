import { env } from "@/lib/env";
import axios from "axios";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import { Game } from "@/types/types";

import { getCurrentUser } from "@/actions/getCurrentUser";

export async function POST(request: NextRequest) {
  try {
    const { username, token } = await getCurrentUser();

    if (!username || !token) {
      return null;
    }
    const { gameId } = await request.json();

    const response = await axios.get(`${env.API_URL}/game/${gameId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.data) {
      const {
        game_id,
        player_one_username,
        player_two_username,
        rows,
        columns,
        board,
        current_turn_username,
        start_time,
        end_time,
        status_name,
      } = response.data;

      const game: Game = {
        gameId: game_id,
        playerOne: player_one_username,
        playerTwo: player_two_username,
        rows: rows,
        cols: columns,
        board: board,
        startTime: start_time,
        endTime: end_time,
        currentTurn: current_turn_username,
        status: status_name,
        username,
      };

      return NextResponse.json({ game }, { status: response.status });
    }
  } catch (error) {
  } finally {
    return NextResponse.json(
      { message: "Error requesting match" },
      { status: 500 },
    );
  }
}
