import authConfig from "@/auth.config";
import NextAuth from "next-auth";

import { env } from "@/lib/env";
import { refreshAccessToken } from "@/lib/utils";
import type { UserToken } from "@/types";
import axios from "axios";

export const {
  handlers: { GET, POST },
  auth,
  signIn,
  signOut: nextAuthSignOut,
} = NextAuth({
  session: {
    strategy: "jwt",
  },
  callbacks: {
    async jwt({ token, user }) {
      // Initial login: Store the tokens
      if (user) {
        const userToken = user as UserToken;

        token.accessToken = userToken.accessToken;
        token.refreshToken = userToken.refreshToken;
        token.player_id = userToken.player_id;
        token.accessTokenExpires = userToken.accessTokenExpires;
      }

      // Return the token if it hasn't expired
      const expiration = token.accessTokenExpires as number;
      if (Date.now() < expiration) {
        return token;
      }

      // Access token has expired, so refresh it
      const newToken = await refreshAccessToken(token);

      return {
        ...token,
        accessToken: newToken.accessToken,
        accessTokenExpires: newToken.accessTokenExpires,
      };
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken;
      session.refreshToken = token.refreshToken;
      session.player_id = token.player_id;

      return session;
    },
  },
  ...authConfig,
});

export async function signOut() {
  try {
    const session = await auth();

    if (!session) {
      throw new Error("No active session");
    }

    // Call external sign-out endpoint
    await axios.post(
      `${env.API_URL}/auth/logout`,
      {
        refresh: session.refreshToken,
      },
      {
        headers: {
          Authorization: `Bearer ${session.accessToken}`,
        },
      },
    );
    // Proceed with NextAuth sign-out
    return nextAuthSignOut();
  } catch (error) {
    return;
  }
}
