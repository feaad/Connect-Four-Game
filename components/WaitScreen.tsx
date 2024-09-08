import React from "react";

const WaitScreen = () => {
  return (
    <div>
      <div className="flex justify-center pt-60">
        <span className="loading loading-dots w-[10rem] bg-white" />
      </div>
      <div className="flex justify-center">
        <h1 className="text-white font-sans text-xl">Waiting for opponent to join</h1>
      </div>
    </div>
  );
};

export default WaitScreen;
