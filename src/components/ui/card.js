import React from "react";
import "../translateUtils.css";

const Card = ({ title, category, description, imageSrc }) => {
  return (
    <div className="mb-20 -hover:translate-y-5 group m-auto mx-10 my-10 mb-0 h-auto min-w-60 max-w-80 transform cursor-pointer rounded-lg border border-indigo-900 bg-indigo-900/25 p-4 shadow-xl shadow-indigo-900 backdrop-blur-sm -backdrop-hue-rotate-90 transition duration-500 ease-in-out perspective-1600 rotate-x-0 hover:scale-105 hover:bg-indigo-900/50 hover:shadow-2xl hover:shadow-indigo-700 hover:rotate-x-12">
      <a href="#" className="block h-full w-full transition">
        {/* <img
          alt="card"
          src={imageSrc}
          className="ty-0 ty-10 mb-5 max-h-60 w-full rounded object-cover transition duration-500"
        /> */}
        <div className="w-full">
          <p className="text-md ty-0 ty-3 font-mono font-medium text-purple-500 transition duration-500">
            {category}
          </p>
          <p className="ty-0 ty-3 mb-2 text-xl font-bold text-white transition duration-500">
            {title}
          </p>
          <p className="text-md ty-0 ty-2 font-serif font-light italic text-indigo-200 transition duration-500">
            {description}
          </p>
        </div>
      </a>
    </div>
  );
};

export default Card;
