import Form from "@/components/Form";
import React from "react";
import Banner from "@/components/Banner";
import Button from "@/components/Button";
import Modal from "./components/Modal";

import { capitalize } from "@/lib/utils";

import Link from "next/link";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import {
  faArrowRight,
  faFaceSmile,
  faGripLinesVertical,
  faHouse,
} from "@fortawesome/free-solid-svg-icons";
import { getCurrentUser } from "@/actions/getCurrentUser";

export default async function Online() {
  const { username } = await getCurrentUser();

  const title = "Play with other Players";


  return (
    <div className="grid h-screen grid-cols-2 gap-16">
      <Banner />
      <div>
        {username ? (
          <div className="gridRight relative">
            <Link
              href="/"
              className="absolute right-0 top-0 m-auto flex flex-row text-slate-400 hover:text-btn-colour"
            >
              <FontAwesomeIcon className="h-5 w-5" icon={faHouse} />
              <p className="pl-2 font-sans">Homepage</p>
            </Link>
            <h1 className="text-2xl font-medium leading-loose">{title}</h1>
            <div className="flex w-full flex-col pt-12">
              <div className="text-2xl">Hello {capitalize(username)}!</div>
              <p className="font-light pt-4">Let's find a worthy opponent </p>
            </div>
          </div>
        ) : (
          <Form title={title} description="First pick a nickname" />
        )}

        <Modal title="Find an opponent" />
      </div>
    </div>
  );
}
