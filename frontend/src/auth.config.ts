import axios from "axios";
import type { NextAuthConfig } from "next-auth";
import Credentials from "next-auth/providers/credentials";

import { LoginSchema } from "@/schemas";

import { env } from "@/lib/env";
import type { UserToken } from "@/types";
import { jwtDecode } from "jwt-decode";

export default {
  providers: [
    Credentials({
      async authorize(credentials) {
        const validatedFields = LoginSchema.safeParse(credentials);

        if (validatedFields.success) {
          const { username, password } = validatedFields.data;

          try {
            const response = await axios.post(`${env.API_URL}/auth/login`, {
              username,
              password,
            });

            const { access, refresh } = response.data;

            if (access && refresh) {
              const decoded: any = jwtDecode(access);

              const response = await axios.get(
                `${env.API_URL}/player?search=${decoded.user_id}`,
              );

              if (response.data.length === 0) {
                return null;
              }

              const { player_id } = response.data[0];

              const user: UserToken = {
                accessToken: access,
                refreshToken: refresh,
                accessTokenExpires: decoded.exp * 1000,
                player_id: player_id,
                username: username,
              };

              return user;
            }
          } catch (error) {
            console.error("Login Failed", error);
            return null;
          }
        }

        return null;
      },
    }),
  ],
} satisfies NextAuthConfig;
