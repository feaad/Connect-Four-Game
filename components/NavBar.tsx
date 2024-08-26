"use client";
import { logout } from '@/actions/logout';
import { faBars } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Link from 'next/link';
import React from 'react'

const NavBar = () => {
  return (
    <div>
      <div className="flex justify-end">
        <details className="dropdown dropdown-end">
          <summary className="btn m-1 border-none bg-white shadow-none">
            <FontAwesomeIcon className="h-5 w-5" icon={faBars} />
          </summary>
          <ul className="p2 w-32 bg-base-00 menu dropdown-content rounded-box shadow">
            <li>
              <Link href="/">Home</Link>
              <Link href="/">Profile</Link>
              <form action={logout}>
                <button
                  type="submit"
                  data-tip="Sign Out"
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
}

export default NavBar