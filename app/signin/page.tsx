import Banner from '@/components/Banner';
import Loading from '@/components/Loading';
import { faEnvelope, faGripLinesVertical, faLock } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import Link from 'next/link';
import React from 'react'

const signin = () => {
  return (
    <main>
      <div className="grid h-screen grid-cols-2 gap-8">
        <Banner />
        <div className="gridRight relative">
          <h1 className="text-2xl font-medium leading-loose">Log In</h1>
          <p className="font-light">Welcome to Connect Four Games</p>
          <div className="pt-12">
            <label className="form-control w-full max-w-xs">
              <div className="label">
                <span className="label-text text-base">Email Address</span>
              </div>
              <label className="input input-bordered flex h-16 w-[40rem] items-center gap-2 rounded border-btn-colour">
                <FontAwesomeIcon
                  icon={faEnvelope}
                  className="h-6 w-6"
                  style={{ color: "#224146" }}
                />
                <FontAwesomeIcon
                  icon={faGripLinesVertical}
                  className="h-5 w-5"
                  style={{ color: "#939393" }}
                />
                <input
                  type="text"
                  className="rounded-lg"
                  placeholder="example@email.com"
                />
              </label>
            </label>
          </div>

          <div className="pt-4">
            <label className="form-control w-full max-w-xs">
              <div className="label">
                <span className="label-text text-base">Password</span>
              </div>
              <label className="input input-bordered flex h-16 w-[40rem] items-center gap-2 rounded border-btn-colour">
                <FontAwesomeIcon
                  icon={faLock}
                  className="h-6 w-6"
                  style={{ color: "#224146" }}
                />
                <FontAwesomeIcon
                  icon={faGripLinesVertical}
                  className="h-5 w-5"
                  style={{ color: "#939393" }}
                />
                <input
                  type="password"
                  className="rounded-lg"
                  placeholder="***********"
                />
              </label>
            </label>
          </div>
          <Loading label={"Log In"} />
          <div className="relative h-[21rem] w-[40rem]">
            <div className="insert-x-0 absolute bottom-0 w-[40rem]">
              <Link
                className="flex flex-row justify-center font-medium text-slate-400"
                href="/signup"
              >
                Don't have an account?
                <p className="pl-1 text-btn-colour">Sign Up</p>
              </Link>
              <div>
                <Link
                  className="flex flex-row justify-center pt-2 font-medium text-slate-400"
                  href="/play-as-guest"
                >
                  Play as guest
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}

export default signin