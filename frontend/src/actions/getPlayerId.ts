"use server";

import { auth } from "@/auth";

export const getPlayerId = async () => {
  const session = await auth();

  return session?.player_id;
};
