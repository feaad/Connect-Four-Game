"use client";
import Banner from "@/components/Banner";
import Loading from "@/components/Loading";
import {
  faEnvelope,
  faGripLinesVertical,
  faHouse,
  faLock,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import React from "react";

import { signIn } from "next-auth/react";

import { useRouter } from "next/navigation";
import { useState } from "react";

const SignIn = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    username: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  async function handleClick() {
    setLoading(true);
    const result = await signIn("credentials", {
      redirect: false,
      username: formData.username,
      password: formData.password,
    });
    setLoading(false);

    if (result?.error) {
      setError("Invalid Credentials");
    } else {
      router.push("/");
    }
  }

  return (
    <main>
      <div className="grid h-screen grid-cols-2 gap-8">
        <Banner />
        <div className="gridRight relative">
          <h1 className="text-2xl font-medium leading-loose">Log In</h1>
          <Link
            href="/"
            className="absolute right-0 top-0 m-auto flex flex-row text-slate-400 hover:text-btn-colour"
          >
            <FontAwesomeIcon className="h-5 w-5" icon={faHouse} />
            <p className="pl-2 font-sans">Homepage</p>
          </Link>
          <p className="font-light">Welcome to Connect Four Games</p>
          <div className="pt-12">
            <label className="form-control w-full max-w-xs">
              <div className="label">
                <span className="label-text text-base">Username</span>
              </div>
              <label className="input input-bordered flex h-16 w-[40rem] items-center gap-2 rounded border-btn-colour">
                <FontAwesomeIcon
                  icon={faEnvelope}
                  className="h-6 w-6"
                  style={{ color: "#224146" }}
                />
                <FontAwesomeIcon
                  icon={faGripLinesVertical}
                  className="h-5 w-5"
                  style={{ color: "#939393" }}
                />
                <input
                  type="text"
                  name="username"
                  placeholder="Username"
                  className="rounded-lg"
                  onChange={handleChange}
                  required
                />
              </label>
            </label>
          </div>

          <div className="pt-4">
            <label className="form-control w-full max-w-xs">
              <div className="label">
                <span className="label-text text-base">Password</span>
              </div>
              <label className="input input-bordered flex h-16 w-[40rem] items-center gap-2 rounded border-btn-colour">
                <FontAwesomeIcon
                  icon={faLock}
                  className="h-6 w-6"
                  style={{ color: "#224146" }}
                />
                <FontAwesomeIcon
                  icon={faGripLinesVertical}
                  className="h-5 w-5"
                  style={{ color: "#939393" }}
                />
                <input
                  type="password"
                  name="password"
                  className="rounded-lg"
                  placeholder="***********"
                  onChange={handleChange}
                  required
                />
              </label>
            </label>
          </div>
          {/* <Loading label={"Log In"} /> */}
          <div className="relative w-[40rem]">
            <div className="flex flex-row">
              <div className="m-auto flex w-3/5 justify-start pt-4">
                {error && (
                  <div className="font-sans font-medium text-rose-600">
                    {error}
                  </div>
                )}
              </div>
              <div className="flex w-2/5 justify-end">
                <div className="pt-4 font-sans font-medium">
                  <button onClick={handleClick}>
                    {loading ? (
                      <span className="insert-y-0 loading loading-dots loading-sm" />
                    ) : (
                      "Log In"
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className="relative h-[21rem] w-[40rem]">
            <div className="insert-x-0 absolute bottom-0 w-[40rem]">
              <Link
                className="flex flex-row justify-center font-medium text-slate-400"
                href="/auth/signup"
              >
                New here?
                <p className="pl-1 text-btn-colour">Sign Up</p>
              </Link>
              <div>
                <Link
                  className="flex flex-row justify-center pt-2 font-medium text-slate-400"
                  href="/play-as-guest"
                >
                  Play as guest
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
};

export default SignIn;
