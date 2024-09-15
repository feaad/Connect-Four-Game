"use client";
import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";

import Banner from "@/components/Banner";
import Form from "@/components/Form";

const ShareLink = () => {
  const router = useRouter();

  const [error, setError] = useState("");
  const [disableBtn, setDisableBtn] = useState(false);

  async function handleClick() {
    setDisableBtn(true);
    setError("");
    try {
      const response = await axios.post("/api/generate-sharelink", {});

      const { shareLink } = response.data;

      if (!shareLink) {
        setDisableBtn(false);
        setError("Failed to Generate link");
        return;
      }

      const linkID = shareLink.split("/").pop();

      router.push(`/sharelink/${linkID}`);
    } catch (error) {
      setDisableBtn(false);
      setError("Failed to Generate link");
    }
  }

  return (
    <div className="grid h-screen grid-cols-2 gap-16">
      <Banner />
      <div>
        <Form title="Play with a friend" description="First pick a nickname" />

        <div className="pt-20">
          <h1 className="font sans pb-2 font-medium">
            Generate and share this link with your friend
          </h1>

          <button
            className="btn btn-block mb-6 h-20 justify-start rounded-lg bg-btn-colour text-base font-normal text-white hover:bg-btn-colour-hover"
            onClick={() => handleClick()}
            disabled={disableBtn}
          >
            Generate Link
          </button>

          <div className="flex h-12 w-full">
            {error && (
              <div className="flex h-full w-full">
                <div className="m-auto font-sans font-medium text-rose-600">
                  {error}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ShareLink;
