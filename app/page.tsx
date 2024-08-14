import React from "react";
import Image from 'next/image';
import connect_four from '../public/images/Connect_four_logo.png';

export default function Home() {
  return (
    <main>
      <div className="grid grid-cols-2 gap-4">
        <div className=" gridLeft font-sans text-5xl text-balance leading-normal">
          <h1>The <br /> Connect Four <br />Game</h1>
          <br/>
          <Image src={connect_four} alt="Connect Four" width={400} height={500} />
        </div>
        
        <div>
          <h1>Hello</h1>
        </div>
        
          
      </div>
      
    </main>
  )
}
