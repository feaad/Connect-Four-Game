"use client";

import {
  faEnvelope,
  faHouse,
  faGripLinesVertical,
} from "@fortawesome/free-solid-svg-icons";
import Loading from "@/components/Loading";
import Banner from "@/components/Banner";
import Link from "next/link";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { signIn } from "next-auth/react";

import { useRouter } from "next/navigation";
import { useState } from "react";

import React from "react";

const GuestPage = () => {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");

  const [loading, setLoading] = useState(false);

  async function handleClick() {
    setLoading(true);
    const result = await signIn("credentials", {
      redirect: false,
      username: username.toLowerCase(),
    });
    setLoading(false);

    if (result?.error) {
      setError("Invalid Credentials");
    } else {
      router.push("/");
    }
  }
  return (
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
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </label>
          </label>
        </div>
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
                    "Let's Play"
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GuestPage;
