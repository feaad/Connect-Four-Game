import { env } from "@/lib/env";
import axios from "axios";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const { username, email, password } = await request.json();

    const user = username.toLowerCase();

    const response = await axios.post(`${env.API_URL}/user/register`, {
      username: user,
      email,
      password,
    });

    return NextResponse.json(response.data);
  } catch (error) {
    return NextResponse.json(
      { message: "Registration failed" },
      { status: 500 },
    );
  }
}
