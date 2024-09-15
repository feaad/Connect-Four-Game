"use server";

import { GameInvitation } from "@/types/types";
import { env } from "@/lib/env";
import axios from "axios";

import { getCurrentUser } from "@/actions/getCurrentUser";

export async function acceptInvitation(
  invitationId: string,
): Promise<string | null> {
  try {
    const { token } = await getCurrentUser();

    if (!token) {
      return null;
    }

    const response = await axios.post(
      `${env.API_URL}/invitation/${invitationId}/accept`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    if (response.data) {
      const { game } = response.data;
      return game;
    }
    return null;
  } catch (error) {
    console.error("Error accepting invitation", error);
    return null;
  }
}
