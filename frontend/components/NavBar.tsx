"use client";
import { getCurrentUser } from "@/actions/getCurrentUser";
import { logout } from "@/actions/logout";
import { faBars, faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import React, { useState } from "react";

const NavBar = () => {
  const [buttonChange, setButtonChange] = useState(false);

  return (
    <div>
      <div className="absolute right-0 top-0 m-auto flex flex-row justify-end">
        <details className="dropdown dropdown-end">
          <summary
            className="btn m-1 border-none bg-white shadow-none"
            onMouseDown={() => setButtonChange(!buttonChange)}
          >
            {buttonChange ? (
              <FontAwesomeIcon className="h-5 w-5" icon={faXmark} />
            ) : (
              <FontAwesomeIcon className="h-5 w-5" icon={faBars} />
            )}
          </summary>
          <ul className="menu dropdown-content z-[1] w-52 rounded-box bg-base-100 p-2 shadow">
            <li>
              <Link className="font-sans text-base" href="/">
                Home
              </Link>
              <Link className="font-sans text-base" href="/">
                Profile
              </Link>
                <form action={logout}>
                  <button
                    type="submit"
                    data-tip="Sign Out"
                    className="font-sans text-base"
                  >
                    Sign Out
                  </button>
                </form>
            </li>
          </ul>
        </details>
      </div>
    </div>
  );
};
export default NavBar;





