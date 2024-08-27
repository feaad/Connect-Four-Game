"use server"

import { auth } from "@/auth";

export const getToken = async () => {
  const session = await auth();

  return session?.accessToken;
};
