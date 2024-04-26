import React from "react";

// Importing all of everything
import Home from "./components/Home.js";

// Importing Router Dom which allows us to link to different pages
import { Route, Routes, useLocation } from "react-router-dom";

function AllRoutes() {
  // Making the website understand where it is
  const location = useLocation();
  return (
    // Making the routes
    <Routes location={location} key={location.pathname}>
      {/* The index is the main page. Whenever the website is loaded, it loads home */}
      <Route index element={<Home />} />

      {/* Placeholder Route*/}
      {/* <Route path="place1" element={<Place1 />} /> */}
    </Routes>
  );
}

export default AllRoutes;
