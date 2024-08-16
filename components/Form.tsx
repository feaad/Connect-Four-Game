import {
  faArrowRight,
  faFaceSmile,
  faGripLinesVertical,
  faHouse,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import React from "react";

interface FormProps {
  title: string;
  description: string;
}

const Form = ({ title, description }: FormProps) => {
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
      <div className="pt-12">
        <label className="form-control w-full max-w-xs">
          <div className="label">
            <span className="label-text text-base">Nickname</span>
          </div>
          <label className="input input-bordered flex h-16 w-[40rem] items-center gap-2 rounded border-btn-colour">
            <FontAwesomeIcon
              icon={faFaceSmile}
              className="h-10 w-10"
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
                <Link href="">
                  <FontAwesomeIcon
                    icon={faArrowRight}
                    className="h-5 w-5"
                    style={{ color: "#224146" }}
                  />
                </Link>
              </div>
            </div>
          </label>
        </label>
      </div>
    </div>
  );
};

export default Form;
