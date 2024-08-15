import React from "react";
import Image from "next/image";
import cfLogo from "@/assets/images/connect_four_logo.svg";
import Buttons from "@/components/Buttons";

import Banner from "@/components/Banner";

export default function Home() {
  return (
    <main>
      <div className="grid h-screen grid-cols-2 gap-16">
        <Banner />

        <div className="gridRight">
          <h1 className="text-2xl font-medium leading-loose">Get Started</h1>
          <p className="font-light">
            Play the Connect Four Game online with players around the world,
            send an invitation link to a friend or play a game with the
            different types of AI!
          </p>
          <br />
          <br />
          <br />
          <div>
            <Buttons />
          </div>
          <br />
          <div className="text-btn-colour link-hover link font-semibold leading-loose">
            <a href="/signup">Sign up</a>
          </div>
          <div className="link-hover link font-medium">
            <a className="font-medium text-slate-400" href="/signin">
              Already have an account?
            </a>
            <a className="text-btn-colour font-semibold" href="/signin">
              {" "}
              Sign in
            </a>
          </div>
        </div>
      </div>
    </main>
  );
}
