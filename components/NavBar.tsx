"use client";
import { logout } from "@/actions/logout";
import { faBars } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Link from "next/link";
import React from "react";

const NavBar = () => {
  return (
    <div>
      <div className="absolute right-0 top-0 m-auto flex flex-row justify-end">
        <details className="dropdown dropdown-end">
          <summary className="btn m-1 border-none bg-white shadow-none">
            <FontAwesomeIcon className="h-5 w-5" icon={faBars} />
          </summary>
          {/* <ul tabIndex={0} className="p2 bg-base-00 menu dropdown-content w-32 rounded-box shadow"> */}
          <ul
            className="menu dropdown-content z-[1] w-52 rounded-box bg-base-100 p-2 shadow"
          >
            <li>
              <Link href="/">Home</Link>
              <Link href="/">Profile</Link>
              <form action={logout}>
                <button type="submit" data-tip="Sign Out">
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
