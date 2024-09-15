import { env } from "@/lib/env";
import { Token } from "@/types/types";
import axios from "axios";
import { jwtDecode } from "jwt-decode";

import type { JWT } from "next-auth/jwt";

export async function refreshAccessToken(token: Token & JWT): Promise<Token> {
    try {
        const response = await axios.post(`${env.API_URL}/token/refresh`, {
            refresh: token.refreshToken,
        });

        const { access: newAccessToken } = response.data;
        const decoded: any = jwtDecode(newAccessToken);

        return {
            ...token,
            accessToken: newAccessToken,
            accessTokenExpires: decoded.exp * 1000, // Set new expiry time
        };
    } catch (error) {
        console.error("Error refreshing access token:", error);
        return {
            ...token,
        };
    }
}

export function capitalize(word: string) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}
