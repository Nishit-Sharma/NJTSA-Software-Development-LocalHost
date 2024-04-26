import logo from "./logo.svg";
import ScrollToTop from "./components/utils/ScrollToTop";
import AllRoutes from "./AllRoutes";
import { BrowserRouter } from "react-router-dom";
import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      {/* This is where everything comes together. It uses the all routes component to know where all of the webpages are and it starts at the index page which is home.js */}
      <AllRoutes />
    </BrowserRouter>
  );
}

export default App;
