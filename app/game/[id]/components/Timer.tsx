"use client";
import { clear } from "console";
import React, { useEffect } from "react";
import { useState } from 'react';


const Timer = () => {
  const [time, setTime] = useState({ minutes: 0, seconds: 0 });

  useEffect(() => {
    const interval = setInterval(() => {
      setTime((prev) => {
        const { minutes, seconds } = prev;

        if (seconds < 59) {
          return { minutes, seconds: seconds + 1 };
        }
        else if (minutes < 59 && seconds === 59) {
          return { minutes: minutes + 1, seconds: 0 };
        } else {
          clearInterval(interval);
          return { minutes: 0, seconds: 0 };
         }
      });
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="pt-20">
      <div className="flex justify-center font-sans text-2xl font-normal">
        Timer
      </div>
      <div className="font-akshar flex justify-center text-[5rem]">
        <p>
          {String(time.minutes).padStart(2, "0")}:{" "}
          {String(time.seconds).padStart(2, "0")}
        </p>
      </div>
    </div>
  );
};

export default Timer;
