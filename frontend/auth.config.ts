import axios from "axios";
import type { NextAuthConfig } from "next-auth";
import Credentials from "next-auth/providers/credentials";

import { UserLoginSchema, GuestLoginSchema } from "@/schemas";
import { env } from "@/lib/env";
import type { UserToken } from "@/types/types";
import { jwtDecode } from "jwt-decode";

async function loginUser(username: string, password: string) {
  try {
    return await axios.post(`${env.API_URL}/auth/login`, {
      username,
      password,
    });
  } catch (error) {
    return null;
  }
}

async function createGuest(username: string) {
  try {
    return await axios.post(`${env.API_URL}/guest/create`, { username });
  } catch (error) {
    return null;
  }
}

async function getPlayer(id: string) {
  try {
    const response = await axios.get(`${env.API_URL}/player?search=${id}`);
    return response.data.length > 0 ? response.data[0] : null;
  } catch (error) {
    return null;
  }
}

async function authorize(credentials: any) {
  const userValidatedFields = UserLoginSchema.safeParse(credentials);
  const guestValidatedFields = GuestLoginSchema.safeParse(credentials);

  const isUser = userValidatedFields.success;
  const isGuest = guestValidatedFields.success;

  if (!isUser && !isGuest) return null;

  let username = "";
  let password = "";

  if (isUser) {
    username = userValidatedFields.data.username;
    password = userValidatedFields.data.password;
  } else if (isGuest) {
    username = guestValidatedFields.data.username;
  }

  const user = username.toLowerCase();

  const response = isUser
    ? await loginUser(user, password)
    : await createGuest(user);
  if (!response || !response.data) return null;

  const { access, refresh } = response.data;
  if (!access || !refresh) return null;

  const decoded: any = jwtDecode(access);
  const id = isUser ? decoded.user_id : decoded.guest_id;

  const player = await getPlayer(id);
  if (!player) return null;

  const userToken: UserToken = {
    accessToken: access,
    refreshToken: refresh,
    accessTokenExpires: decoded.exp * 1000,
    player_id: player.player_id,
    username: user,
    ...(isUser ? { user_id: id } : { guest_id: id }),
  };

  return userToken;
}

export default {
  providers: [Credentials({ authorize })],
} satisfies NextAuthConfig;
