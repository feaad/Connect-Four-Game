"use client";
import {
  faArrowRight,
  faFaceSmile,
  faGripLinesVertical,
  faHouse,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import React, { useState } from "react";

interface FormProps {
  title: string;
  description: string;
  onClick?: () => void;
}

const Form = ({ title, description }: FormProps) => {
  const [loading, setLoading] = useState(false);

  function saveData() {
    // Send data to server for Guest Registration

    // Open A websocket Connection


    // Send data to server
    setLoading(true);
    // <div className="alert alert-success">Data saved</div>
    setTimeout(() => {
      setLoading(false);
    }, 5000);
    console.log("Data saved");
  }
  return (
    <div className="gridRight relative">
      <Link
        href="/"
        className="absolute right-0 top-0 m-auto flex flex-row text-slate-400 hover:text-btn-colour"
      >
        <FontAwesomeIcon className="h-5 w-5" icon={faHouse} />
        <p className="pl-2 font-sans">Homepage</p>
      </Link>
      <h1 className="text-2xl font-medium leading-loose">{title}</h1>
      <p className="font-light">{description}</p>
      <div className="pt-12 w-full flex">
        <label className="form-control w-full flex">
          <div className="label">
            <span className="label-text text-base">Nickname</span>
          </div>
          <label className="input input-bordered flex h-16 items-center gap-2 rounded border-btn-colour">
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
              placeholder="Enter your nickname"
            />
            <div className="relative w-full">
              <div className="flex flex-row justify-end">
                  <button onClick={saveData}>
                    {loading ? (
                      "Saving..."
                    ) : (
                      <FontAwesomeIcon
                        icon={faArrowRight}
                        className="h-5 w-5"
                        style={{ color: "#224146" }}
                      />
                    )}
                  </button>

              </div>
            </div>
          </label>
        </label>
      </div>
    </div>
  );
};

export default Form;
