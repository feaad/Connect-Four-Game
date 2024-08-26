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

  async function handleClick() {
    await axios.post(
      `${env.API_URL}/match/request`,
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      },
    );
  }

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
            {/* <div className="flex w-full flex-col pt-12">
              <div className="text-2xl">Hello {capitalize(username)}!</div>
              <p className="pt-4 font-light">
                To play online with others find a worthy opponent{" "}
              </p>
            </div> */}
          </div>
        ) : (
          <Form
            title={title}
            description="First pick a nickname"
            onClick={handleClick}
          />
        )}

        <Modal title="Find an opponent" />
      </div>
    </div>
  );
}
