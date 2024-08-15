import Image from "next/image";
import cfLogo from "@/assets/images/connect_four_logo.svg";

const Banner = () => {
  return (
    <div>
      <div className="m-auto flex h-[90vh] w-full">
        <div className="bg-bgc m-auto flex h-full w-full flex-col rounded-2xl pl-9">
          <div className="h-1/4 w-full flex-col text-balance pt-14 text-left font-sans text-5xl leading-normal text-black">
            <h1 className="m-auto h-full w-full">
              The <br /> Connect Four <br />
              Game
            </h1>
          </div>
          <div className="m-auto flex h-3/4 w-full flex-col">
            <Image
              src={cfLogo}
              alt="Connect Four"
              width={517.77}
              height={433}
              className="my-auto"
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Banner;
