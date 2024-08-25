"use client";
import axios from "axios";

import React from "react";
import Banner from "@/components/Banner";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHouse } from "@fortawesome/free-solid-svg-icons";
import { faFaceSmile } from "@fortawesome/free-solid-svg-icons";
import Link from "next/link";
import { faGripLinesVertical } from "@fortawesome/free-solid-svg-icons";
import { faEnvelope } from "@fortawesome/free-solid-svg-icons";
import { faLock } from "@fortawesome/free-solid-svg-icons";

import { useRouter } from "next/navigation";
import { useState } from "react";

const SignUp = () => {
  const router = useRouter();
  const [formData, setFormData] = useState({
    email: "",
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
    try {
      setLoading(true);
      await axios.post("/api/auth/register", formData);
      setLoading(false);
      router.push("/login");
    } catch (error) {
      setLoading(false);
      setError("Registration failed");
    }
  }

  return (
    <main>
      <div className="grid h-screen grid-cols-2 gap-8">
        <Banner />
        <div className="gridRight relative">
          <Link
            href="/"
            className="absolute right-0 top-0 m-auto flex flex-row text-slate-400 hover:text-btn-colour"
          >
            <FontAwesomeIcon className="h-5 w-5" icon={faHouse} />
            <p className="pl-2 font-sans">Homepage</p>
          </Link>

          <h1 className="text-2xl font-medium leading-loose">Sign Up</h1>
          <p className="font-light">
            Sign up to access more and save your wins!
          </p>
          <div className="pt-12">
            <label className="form-control w-full max-w-xs">
              <div className="label">
                <span className="label-text text-base">Username</span>
              </div>
              <label className="input input-bordered flex h-16 w-[40rem] items-center gap-2 rounded border-btn-colour">
                <FontAwesomeIcon
                  icon={faFaceSmile}
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
                  className="rounded-lg"
                  placeholder="Enter your nickname"
                  onChange={handleChange}
                  required
                />
              </label>
            </label>
          </div>
          <div className="pt-4">
            <label className="form-control w-full max-w-xs">
              <div className="label">
                <span className="label-text text-base">Email Address</span>
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
                  type="email"
                  name="email"
                  className="rounded-lg"
                  placeholder="example@email.com"
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
                <div className="flex pt-4 font-sans font-medium">
                  <button onClick={handleClick}>
                    {loading ? (
                      <span className="insert-y-0 loading loading-dots loading-sm"></span>
                    ) : (
                      "Sign Up"
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className="relative h-[13rem] w-[40rem]">
            <div className="insert-x-0 absolute bottom-0 w-[40rem]">
              <Link
                className="flex flex-row justify-center font-medium text-slate-400"
                href="/auth/signin"
              >
                Already have an account?{" "}
                <p className="pl-1 text-btn-colour">Sign In</p>
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

export default SignUp;
