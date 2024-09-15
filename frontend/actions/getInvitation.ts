"use server";

import { GameInvitation } from "@/types/types";
import { env } from "@/lib/env";
import axios from "axios";

import { getCurrentUser } from "@/actions/getCurrentUser";

export async function getInvitation(
  invitationId: string,
): Promise<GameInvitation | null> {
  try {
    const { username, token } = await getCurrentUser();

    if (!username || !token) {
      return null;
    }

    const response = await axios.get(
      `${env.API_URL}/invitation/share-invite/${invitationId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    if (response.data) {
      const {
        invitation_id,
        sender_username,
        receiver_username,
        status_name,
        game,
        play_preference,
        rows,
        columns,
      } = response.data;

      const invite: GameInvitation = {
        invitationId: invitation_id,
        gameId: game,
        sender: sender_username,
        receiver: receiver_username,
        status: status_name,
        playPreference: play_preference,
        rows: rows,
        cols: columns,
        username,
      };

      return invite;
    }
    return null;
  } catch (error) {
    return null;
  }
}
