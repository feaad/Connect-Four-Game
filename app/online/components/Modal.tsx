"use client";
import { clear } from "console";
import React, { useEffect, useState } from "react";
import Form from "@/components/Form";

// import useWebSocket from "@/hooks/useWebSocket";

import {
  faFaceSmile,
  faGripLinesVertical,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface ModalProps {
  title: string;
  onClick?: () => void;
}

const Modal = ({ title }: ModalProps) => {
  const [messages, setMessages] = useState<string[]>([]);
  const [isVisible, setIsVisible] = useState(false);

  // const playerId = "d40dd383-c034-4a12-8e14-4496a2ee8659";
  // const token =
  //   "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzIzOTE1MTg4LCJpYXQiOjE3MjM5MTQ4ODgsImp0aSI6ImJiMjA4ODVkYjc3ZTRiZjc5MTk4YzA4ZTYwMDQ2ZDI3IiwidXNlcl9pZCI6ImQwYTNmNWM3LWNiYWMtNDQ5Mi04MjUyLWJmYzNlNDhkMDRjYSJ9.MIkEZtn9Z3ut3_7QFKWXIHg6ZqpvPz5ydblxWZpkknA";
  // // Callback function to handle incoming messages
  // const handleMessage = (data: any) => {
  //   if (data.message) {
  //     setMessages((prev) => [...prev, data.message]);
  //   }
  // };

  // Use the custom WebSocket hook
  // const { sendMessage, isConnected } = useWebSocket({
  //   url: "http://localhost:9080/ws/player/" + playerId,
  //   token: token,
  //   onMessage: handleMessage,
  // });

  useEffect(() => {
    setIsVisible(true);

    const timer = setTimeout(() => {
      setIsVisible(false);
    }, 5000);
  }, []);

  function handleModalOnClick() {
    const modal = document.getElementById("modal");

    if (modal) {
      const modal = document.getElementById("modal") as HTMLDialogElement;

      modal.showModal();
    }
  }
  return (
    <div className="flex w-full pt-12">
      <button
        className="btn btn-block mb-6 h-20 justify-start rounded-lg bg-btn-colour text-base font-normal text-white hover:bg-btn-colour-hover"
        onClick={() => handleModalOnClick()}
      >
        {title}
      </button>
      <dialog id="modal" className="modal">
        <div className="modal-box h-[10rem] w-11/12 max-w-xl">
          <div className="relative m-auto flex h-[3rem] w-[30rem]">
            <div className="absolute">
              {isVisible ? (
                <div className="relative float-right h-[3rem] w-[30rem]">
                  <span className="label-text flex justify-center text-base">
                    Searching for opponent...
                  </span>
                  <div className="absolute flex h-[3rem] w-[30rem] justify-center">
                    <span className="loading loading-ring loading-lg bottom-0 pt-20"></span>
                  </div>
                </div>
              ) : (
                <div>
                  <label className="form-control w-full max-w-xs">
                    <div className="label">
                      <span className="label-text flex justify-center text-base">
                        Your Opponent
                      </span>
                    </div>
                    <label className="input input-bordered flex h-16 w-[30rem] items-center gap-2 rounded border-btn-colour">
                      <FontAwesomeIcon
                        icon={faFaceSmile}
                        className="h-6 w-6"
                        style={{ color: "#224146" }}
                      />
                      <FontAwesomeIcon
                        icon={faGripLinesVertical}
                        className="h-5 w-5"
                        style={{ color: "#939393" }}
                      />
                      <input
                        type="text"
                        className="rounded-lg"
                        placeholder="Suka"
                        disabled
                      />
                    </label>
                  </label>
                </div>
              )}
            </div>
          </div>
        </div>
        <form method="dialog" className="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </div>
  );
};

export default Modal;
