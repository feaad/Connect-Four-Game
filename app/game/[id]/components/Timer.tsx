"use client";

import { observer } from "mobx-react-lite";

import React, { useEffect, useState } from "react";
import { GridStoreProps } from "../GridStore";

interface TimerProps {
  store: GridStoreProps;
}

const Timer = observer(({ store }: TimerProps) => {
  const [time, setTime] = useState({ minutes: 0, seconds: 0 });

  const calculateTimeDelta = (startTime: Date, endTime?: Date) => {
    const currentTime = endTime || new Date();
    const delta = currentTime.getTime() - startTime.getTime();
    const hours = Math.floor(
      (delta % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60),
    );
    const minutes = Math.floor((delta % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((delta % (1000 * 60)) / 1000);
    return { hours, minutes, seconds };
  };

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    let startDate: Date | null = null;
    let endDate: Date | null = null;

    if (store.game.startTime) {
      startDate = new Date(store.game.startTime);
    }

    if (store.game.endTime) {
      endDate = new Date(store.game.endTime);
    }

    if (startDate && !endDate) {
      interval = setInterval(() => {
        const { minutes, seconds } = calculateTimeDelta(startDate);
        setTime({ minutes, seconds });
      }, 1000);
    } else if (startDate && endDate) {
      const { minutes, seconds } = calculateTimeDelta(startDate, endDate);
      setTime({ minutes, seconds });
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [store.game.startTime, store.game.endTime]);

  return (
    <div className="pt-20">
      <div className="flex justify-center font-sans text-3xl font-normal text-white">
        Timer
      </div>
      <div className="flex justify-center font-akshar text-[13rem] text-white">
        <p>
          {String(time.minutes).padStart(2, "0")}:{" "}
          {String(time.seconds).padStart(2, "0")}
        </p>
      </div>
    </div>
  );
});

export default Timer;
