import Form from "@/components/Form";
import React from "react";
import Banner from "@/components/Banner";
import Button from "@/components/Button";
import Modal from "./components/Modal";

const page = () => {
  return (
    <div className="grid h-screen grid-cols-2 gap-16">
      <Banner />
      <div>
        <Form
          title="Play with other Players"
          description="First pick a nickname"
        />

        <Modal title="Find an opponent" />
      </div>
    </div>
  );
};

export default page;
