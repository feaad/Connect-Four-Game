import { env } from "@/lib/env";
import axios from "axios";
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const { username, email, password } = await request.json();

    console.log("Creating user with username:", username);
    const response = await axios.post(`${env.API_URL}/user/register`, {
      username,
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
