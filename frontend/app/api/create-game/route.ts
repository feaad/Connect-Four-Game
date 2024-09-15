import { env } from "@/lib/env";
import axios from "axios";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

import { getCurrentUser } from "@/actions/getCurrentUser";
import { Game } from "@/types/types";

export async function POST(request: NextRequest) {
    try {
        const { token } = await getCurrentUser();

        const { difficulty_level, algorithm } = await request.json();

        const response = await axios.post(
            `${env.API_URL}/game/create`,
            {
                difficulty_level,
                algorithm,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            },
        );

        if (response.data) {
            const { game_id } = response.data;

            return NextResponse.json({ game_id }, { status: response.status });
        }
    } catch (error) {
        console.error(error);
        return NextResponse.json(
            { message: "Error creating game" },
            { status: 500 },
        );
    }
}
