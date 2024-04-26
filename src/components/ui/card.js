import React from "react";

const Card = ({ title, category, description, imageSrc }) => {
  return (
    <div className="m-auto mx-10 my-10 h-auto min-w-60 max-w-80 transform cursor-pointer overflow-hidden rounded-lg border border-indigo-900 bg-indigo-900/25 p-4 shadow-xl shadow-indigo-900 transition duration-500 ease-in-out hover:translate-y-5 hover:scale-95 hover:bg-indigo-900/50 hover:shadow-lg hover:shadow-indigo-700">
      <a href="#" className="block h-full w-full">
        <img
          alt="card image"
          src={imageSrc}
          className="max-h-60 w-full object-cover"
        />
        <div className="w-full">
          <p className="text-md font-mono font-medium text-purple-500">
            {category}
          </p>
          <p className="mb-2 text-xl font-bold text-white">{title}</p>
          <p className="text-md font-serif font-light italic text-indigo-200">
            {description}
          </p>
        </div>
      </a>
    </div>
  );
};

export default Card;
