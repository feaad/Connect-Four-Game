import * as z from "zod";

export const LoginSchema = z.object({
  username: z.string().min(5, {
    message: "Username is required",
  }),
  password: z.string().min(6, {
    message: "Password is required",
  }),
});

export const RegisterSchema = z.object({
  username: z.string().min(5, {
    message: "Username is required",
  }),
  email: z.string().email({
    message: "Email is required",
  }),
  password: z.string().min(6, {
    message: "Minimum 6 characters required",
  }),
});
