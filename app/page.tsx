import React from "react";
import Button from "@/components/Button";

import Banner from "@/components/Banner";
import Link from "next/link";


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
          
          <div className="pt-12">
            <Button
              label="Play online with other players"
              link="online"
            />
            <Button
              label="Send a link to play with a friend"
              link="/send-link"
            />
            <Button label="Play with our AI" link="/play-ai" />
          </div>
          <br />
          <div className="text-btn-colour link-hover link font-semibold leading-loose">
            <Link href="/signup">Sign up</Link>
          </div>
          <div className="link-hover link font-medium">
            <Link className="font-medium text-slate-400" href="/signin">
              Already have an account?
            </Link>
            <Link className="text-btn-colour font-semibold" href="/signin">
              {" "}
              Sign in
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
