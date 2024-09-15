"use server";

import { env } from "@/lib/env";

export const getWSUrl = async () => {
  return env.WS_URL;
};
