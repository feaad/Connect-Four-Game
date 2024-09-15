import { env } from "@/lib/env";
import axios from "axios";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { getCurrentUser } from "@/actions/getCurrentUser";
import { Game } from "@/types/types";

import { encodeUUID } from "@/lib/transformer";

export async function POST(request: NextRequest) {
  try {
    const { username, token } = await getCurrentUser();

    const response = await axios.post(
      `${env.API_URL}/invitation/generate`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );

    if (response.data) {
      const { invitation_id } = response.data;

      if (!invitation_id) {
        return NextResponse.json(
          { message: "Error generating share link" },
          { status: 500 },
        );
      }

      return NextResponse.json(
        {
          shareLink: `${env.NEXTAUTH_URL}/sharelink/${encodeUUID(invitation_id)}`,
        },
        { status: response.status },
      );
    }
  } catch (error) {
    console.error(error);
    return NextResponse.json(
      { message: "Error generating share link" },
      { status: 500 },
    );
  }
}
