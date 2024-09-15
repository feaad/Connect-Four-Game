import Form from "@/components/Form";
import React from "react";
import Banner from "@/components/Banner";
import Button from "@/components/Button";
import Modal from "./components/Modal";

import { capitalize } from "@/lib/utils";
import { logout } from "@/actions/logout";

import Link from "next/link";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import axios from "axios";
import { env } from "@/lib/env";

import {
  faArrowRight,
  faFaceSmile,
  faGripLinesVertical,
  faHouse,
} from "@fortawesome/free-solid-svg-icons";

import NavBar from "@/components/NavBar";
import { getCurrentUser } from "@/actions/getCurrentUser";

export default async function Online() {
  const { username, playerId, token } = await getCurrentUser();

  const title = "Play Online with Others";

  return (
    <div className="grid h-screen grid-cols-2 gap-16">
      <Banner />
      <div>
        {username ? (
          <div className="gridRight relative">
            <NavBar />
            <h1 className="text-2xl font-medium leading-loose">{title}</h1>
            <p className="pt-2 font-light">
              To play online with others find an opponent{" "}
            </p>
          </div>
        ) : (
          <Form title={title} description="First pick a nickname" />
        )}

        {playerId && <Modal title="Find an opponent" playerId={playerId} />}
      </div>
    </div>
  );
}
