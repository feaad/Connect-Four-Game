import React from "react";
import Banner from "@/components/Banner";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHouse } from "@fortawesome/free-solid-svg-icons";
import Link from "next/link";


const signup = () => {
  return (
    <main>
      <div className="grid h-screen grid-cols-2 gap-8">
        <Banner />
        <div className="gridRight relative">
          <Link
            href="/"
            className="absolute right-0 top-0 m-auto flex flex-row"
          >
            <FontAwesomeIcon className="h-5 w-5" icon={faHouse} />
            <p className="pl-2">Homepage</p>
          </Link>
        </div>
      </div>
    </main>
  );
};

export default signup;
