import React from "react";

const SwitchButton = ({
  primaryStyles = "border-indigo-500 bg-indigo-500/50 hover:bg-indigo-400 hover:shadow-indigo-400 hover:ring-2 hover:ring-indigo-300 hover:ring-offset-2",
  secondaryStyles = "border-pink-500 bg-pink-500/50 hover:bg-pink-400 hover:shadow-pink-400 hover:ring-2 hover:ring-pink-300 hover:ring-offset-2",
  text,
  isActive,
  onClick,
}) => {
  return (
    <button
      onClick={onClick}
      className={`group relative overflow-hidden rounded-lg border px-8 py-2 font-mono italic text-white shadow-lg transition-all duration-300 ease-out ${
        isActive ? secondaryStyles : primaryStyles
      }`}
    >
      <span className="ease absolute right-0 -mt-12 h-32 w-8 translate-x-12 rotate-12 transform bg-white opacity-20 transition-all duration-1000 group-hover:-translate-x-40"></span>
      <span className="relative font-medium">{text}</span>
    </button>
  );
};

export default SwitchButton;
