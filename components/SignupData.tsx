"use client";
import Link from "next/link";
import React, { useState } from "react";
import Modal from "./Modal";

interface LoadingProps {
  label: string;
  onClick?: () => void;
}

const SignupData = ({ label }: LoadingProps) => {
  const [loading, setLoading] = useState(false);

  function handleClick() {
    // fetch data
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 5000);
  }
  return (
    <div className="relative w-[40rem]">
      <div className="flex flex-row justify-end">
        <Link href="" className="pt-4 font-sans font-medium">
          <button onClick={handleClick}>
            {loading ? (
              <span className="insert-y-0 loading loading-dots loading-sm"></span>
            ) : (
              label
            )}
          </button>
        </Link>
  </div>
    </div>
  );
};

export default SignupData;
