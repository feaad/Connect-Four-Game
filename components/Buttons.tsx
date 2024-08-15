import React from "react";

const Buttons = () => {
  const buttons = [
    { label: "Play online with other players", link: "/play-online" },
    { label: "Send a link to play with a friend", link: "/send-link" },
    { label: "Play with our AI", link: "/play-ai" },
  ];
  return (
    <div>
      <div>
        {buttons.map((button, index) => (
          <button
            key={button.link}
            className="bg-btn-colour hover:bg-btn-colour-hover btn btn-block mb-6 h-20 justify-start rounded-lg text-base font-normal text-white"
          >
            {button.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Buttons;
