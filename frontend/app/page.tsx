import React from "react";
import Button from "@/components/Button";

import Banner from "@/components/Banner";
import Link from "next/link";
import { getCurrentUser } from "@/actions/getCurrentUser";
import NavBar from "@/components/NavBar";

export default async function Home() {
  const { playerId } = await getCurrentUser();

  return (
    <main>
      <div className="grid h-screen grid-cols-2 gap-16">
        <Banner />
        <div className="gridRight relative">
          {playerId && <NavBar />}

          <h1 className="text-2xl font-medium leading-loose">Get Started</h1>
          <p className="font-light">
            Play the Connect Four Game online with players around the world,
            send an invitation link to a friend or play a game with the
            different types of AI!
          </p>

          <div className="pt-12">
            <Button label="Play online with other players" link="online" />
            <Button
              label="Send a link to play with a friend"
              link="/sharelink"
            />
            <Button label="Play with our AI" link="/ai" />
          </div>

          {!playerId && (
            <>
              <br />
              <div className="link-hover link font-semibold leading-loose text-btn-colour">
                <Link href="/auth/signup">Sign up</Link>
              </div>
              <div className="link-hover link font-medium">
                <Link
                  className="font-medium text-slate-400"
                  href="/auth/signin"
                >
                  Already have an account?
                </Link>
                <Link
                  className="font-semibold text-btn-colour"
                  href="/auth/signin"
                >
                  {" "}
                  Log in
                </Link>
              </div>
            </>
          )}
        </div>
      </div>
    </main>
  );
}
