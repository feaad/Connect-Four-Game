"use server";

import { auth } from "@/auth";

export const getCurrentUser = async () => {
  const session = await auth();

  return {
    username: session?.username,
    playerId: session?.player_id,
  }
};
