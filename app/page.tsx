import React from "react";
import Image from "next/image";
import cfLogo from "@/assets/images/connect_four_logo.svg";

import Banner from "@/components/Banner";

export default function Home() {
  return (
    <main>
      {/* <div className="grid grid-cols-2 gap-8">
        <div className=" gridLeft font-sans text-5xl text-balance leading-normal">
          <h1>The <br /> Connect Four <br />Game</h1>
          <br/>
          <Image src={cfLogo} alt="Connect Four" width={400} height={500} />
        </div>


        <div className="gridRight ">
          <h1 className="text-2xl font-medium leading-loose">Get Started</h1>
          <p className="font-light">Play the Connect Four Game online with players around the
            world, send an invitation link to a friend or play a game with the different types
            of AI!</p>
          <br />
          <div>
            <button className="btn btn-block">Play Now</button>
          </div>
        </div>

      </div> */}

      <div className="grid h-screen grid-cols-2 gap-8">
        <Banner />

        <div className="gridRight">
          <h1 className="text-2xl font-medium leading-loose">Get Started</h1>
          <p className="font-light">
            Play the Connect Four Game online with players around the world,
            send an invitation link to a friend or play a game with the
            different types of AI!
          </p>
          <br />
          <div>
            <button className="btn btn-block bg-btn-colour text-white">Play Now</button>
          </div>
        </div>
      </div>
    </main>
  );
}
