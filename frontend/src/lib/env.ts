import { z } from "zod";

const envSchema = z.object({
  API_URL: z.string().url({
    message: "API_URL must be a valid URL",
  }),
  WS_URL: z.string().url({
    message: "WS_URL must be a valid URL",
  }),

  NEXTAUTH_SECRET: z.string().min(1, "The NextAuth Secret is Required"),

  NEXTAUTH_URL: z.string().url({
    message: "NEXTAUTH_URL must be a valid URL",
  }),
});



export const env = envSchema.parse(process.env);
