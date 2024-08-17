'use client';
import React from "react";

const Modal = () => {
  return (
    <div>
      <button
        className="btn"
        onClick={() => document.getElementById("modal").showModal()}
      >
        open modal
      </button>
      <dialog id="modal" className="modal">
        <div className="modal-box">
          <h3 className="text-lg font-bold">Hello!</h3>
          <p className="py-4">Press ESC key or click outside to close</p>
        </div>
        <form method="dialog" className="modal-backdrop">
          <button>close</button>
        </form>
      </dialog>
    </div>
  );
};

export default Modal;
