"use client";
import React, { useEffect, useState } from "react";
import axios from "axios";

import Button from "@/components/Button";
import { useRouter } from "next/navigation";

interface ModalProps {
  algorithm: string;
}

interface Levels {
  level: number;
  label: string;
}

function capitalize(word: string) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}

const Modal = ({ algorithm }: ModalProps) => {
  const router = useRouter();
  const [error, setError] = useState("");
  const [disableBtn, setDisableBtn] = useState(false);

  const levels: Levels[] = [
    { level: 1, label: "Rookie" },
    { level: 2, label: "Scout" },
    { level: 3, label: "Explorer" },
    { level: 4, label: "Champion" },
    { level: 5, label: "Legend" },
  ];

  function openModal(algo: string) {
    const modalName = `modal-${algo}`;
    const modal = document.getElementById(modalName);

    if (modal) {
      const modal = document.getElementById(modalName) as HTMLDialogElement;
      modal.showModal();
    }
  }

  async function handleClick(difficulty_level: number) {
    setDisableBtn(true);
    try {
      const response = await axios.post("/api/create-game", {
        difficulty_level,
        algorithm,
      });

      const { game_id } = response.data;

      if (!game_id) {
        setDisableBtn(false);
        setError("Failed to request game");
        return;
      }

      router.push(`/game/${game_id}`);
    } catch (error) {
      setDisableBtn(false);
      setError("Failed to request game");
    }
  }

  return (
    <div>
      <button
        onClick={() => openModal(algorithm)}
        className="btn btn-block mb-6 h-20 justify-start rounded-lg bg-btn-colour text-base font-normal text-white hover:bg-btn-colour-hover"
      >
        {capitalize(algorithm)}
      </button>
      <dialog
        id={`modal-${algorithm}`}
        className="modal modal-bottom sm:modal-middle"
      >
        <div className="modal-box">
          <h3 className="flex justify-center pb-5 font-sans text-lg">
            Pick a level
          </h3>
          {error && (
            <div className="flex w-full">
              <div className="m-auto font-sans font-medium text-rose-600">
                {error}
              </div>
            </div>
          )}

          {levels.map(({ level, label }) => (
            <button
              className="btn btn-block mb-6 h-20 justify-start rounded-lg bg-btn-colour text-base font-normal text-white hover:bg-btn-colour-hover"
              onClick={() => handleClick(level)}
              key={level}
              disabled={disableBtn}
            >
              {`Level ${level} - ${label}`}
            </button>
          ))}
        </div>
        <form method="dialog" className="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </div>
  );
};

export default Modal;
