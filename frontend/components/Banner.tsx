import Image from "next/image";
import cfLogo from "@/assets/images/connect_four_logo.svg";
import Head from "next/head";

const Banner = () => {
  return (
    <div>
      <div className="m-auto flex h-[90vh] w-full">
        <div className="flex h-full w-5/6 flex-col rounded-2xl bg-bgc pl-5">
          <div className="h-1/4 w-full flex-col text-balance pb-52 pt-14 text-left font-sans text-5xl leading-normal text-black">
            <h1 className="m-auto h-full w-full">
              The <br /> Connect Four <br />
              Game
            </h1>
          </div>
          <div className="flex pt-4">
            <div className="flex md:max-w-2xl">
              <div className="m-auto flex h-3/4 w-full flex-col">
                <Image
                  src={cfLogo}
                  alt="Connect Four"
                  // width= {20}
                  // height={20}
                  className="m-auto"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Banner;
