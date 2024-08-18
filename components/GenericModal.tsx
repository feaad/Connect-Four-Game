"use client";
import React from "react";
import Button from "./Button";
interface GenericModalProps {
  title: string;
}

const GenericModal = ({ title }: GenericModalProps) => {
  function openModal() {
    const modal = document.getElementById("modal");

    if (modal) {
      const modal = document.getElementById("modal") as HTMLDialogElement;

      modal.showModal();
    }
  }
  return (
    <div>
      <button
        onClick={() => openModal()}
        className="btn btn-block mb-6 h-20 justify-start rounded-lg bg-btn-colour text-base font-normal text-white hover:bg-btn-colour-hover"
      >
        {title}
      </button>
      <dialog id="modal" className="modal modal-bottom sm:modal-middle">
        <div className="modal-box">
          <h3 className="pb-5 font-sans text-lg">Pick a level</h3>
          <Button label="Level 1 - Rookie" link="/game" />
          <Button label="Level 2 - Scout" link="/game" />
          <Button label="Level 3 - Explorer" link="/game" />
          <Button label="Level 4 - Champion" link="/game" />
          <Button label="Level 5 - Legend" link="/game" />
        </div>
        <form method="dialog" className="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </div>
  );
};

export default GenericModal;
