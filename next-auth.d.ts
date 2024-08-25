import NextAuth from "next-auth";

import { Token } from "@/types/types";

declare module "next-auth" {
    interface Session extends Token {}
}

declare module "next-auth/jwt" {
	interface JWT extends Token {}
}