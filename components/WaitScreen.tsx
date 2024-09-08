import React from "react";
interface WaitScreenProps {
  title: string;
}

const WaitScreen = ({ title }: WaitScreenProps) => {
  return (
    <div>
      <div className="flex justify-center pt-60">
        <span className="loading loading-dots w-[10rem] bg-white" />
      </div>
      <div className="flex justify-center">
        <h1 className="font-sans text-xl text-white">{title}</h1>
      </div>
    </div>
  );
};

export default WaitScreen;
