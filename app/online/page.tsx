import Form from "@/components/Form";
import React from "react";
import Banner from "@/components/Banner";

const page = () => {
  return (
    <div className="grid h-screen grid-cols-2 gap-16">
      <Banner />
      <Form
        title="Play with other Players"
        description="First pick a nickname"
      />
    </div>
  );
};

export default page;
