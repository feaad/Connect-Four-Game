"use client";
import axios from "axios";

import React, { useEffect, useState } from "react";
import useWebSocket, { UseWebSocketProps } from "@/hooks/useWebSocket";
import { useRouter } from "next/navigation";

interface ModalProps {
  title: string;
  playerId: string;
}

const Modal = ({ title, playerId }: ModalProps) => {
  const router = useRouter();
  const [isVisible, setIsVisible] = useState(false);
  const [error, setError] = useState("");

  const [webSocketConfig, setWebSocketConfig] =
    useState<UseWebSocketProps | null>(null);

  const { receivedMessage, connectionStatus } = useWebSocket({
    path: "/player/" + playerId,
  });


  async function handleClick() {
    setIsVisible(true);
    try {
      await axios.post("/api/request-match", {});
    } catch (error) {
      setIsVisible(false);
      setError("Cannot find opponent.");
    }
  }

 
  /* The `useEffect` hook in the provided code snippet is responsible for handling side effects in the
component. In this case, it is triggered whenever the `receivedMessage` state
variable changes. */
  useEffect(() => {
    if (receivedMessage) {
      const message = JSON.parse(receivedMessage);

      if (message.message && message.message.game_id) {
        router.push("/game/" + message.message.game_id);
      }
    }
  }, [receivedMessage]);

  return (
    <div>
      <div className="flex w-full pt-12">
        <button
          className="btn btn-block mb-6 h-20 justify-start rounded-lg bg-btn-colour text-base font-normal text-white hover:bg-btn-colour-hover"
          onClick={handleClick}
        >
          {isVisible ? "Searching for opponent..." : title}
        </button>
      </div>
      {error && (
        <div className="flex w-full">
          <div className="m-auto font-sans font-medium text-rose-600">
            {error}
          </div>
        </div>
      )}
      <div id="loading">
        <div>
          {isVisible && (
            <div>
              <div className="relative flex justify-center">
                <div className="justify-center">
                  <span className="loading loading-ring loading-lg bottom-0 pt-20" />
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Modal;
