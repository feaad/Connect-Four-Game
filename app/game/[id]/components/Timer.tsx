"use client";
import React, { useEffect } from "react";
import { useState } from "react";

interface TimerProps {
  startDate: Date | null;
  endDate: Date | null;
}

const Timer = ({ startDate, endDate }: TimerProps) => {
  const [time, setTime] = useState({ minutes: 0, seconds: 0 });

  const calculateTimeDelta = (startTime: Date, endTime?: Date) => {
    const currentTime = endTime || new Date();

    const delta = currentTime.getTime() - startTime.getTime();
    const hours = Math.floor(delta / 3600000);
    const minutes = Math.floor(delta / 60000);
    const seconds = Math.floor((delta % 60000) / 1000);

    return { hours, minutes, seconds };
  };

  useEffect(() => {
    if (startDate && !endDate) {
      const interval = setInterval(() => {
        const { minutes, seconds } = calculateTimeDelta(startDate);
        setTime({ minutes, seconds });
      }, 1000);

      return () => clearInterval(interval);
    } else if (startDate && endDate) {
      const { minutes, seconds } = calculateTimeDelta(startDate, endDate);
      setTime({ minutes, seconds });
    }
  }, [startDate, endDate]);

  return (
    <div className="pt-20">
      <div className="flex justify-center font-sans text-2xl font-normal">
        Timer
      </div>
      <div className="flex justify-center font-akshar text-[5rem]">
        <p>
          {String(time.minutes).padStart(2, "0")}:{" "}
          {String(time.seconds).padStart(2, "0")}
        </p>
      </div>
    </div>
  );
};

export default Timer;
