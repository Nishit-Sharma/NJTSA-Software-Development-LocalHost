import React, { useState, useEffect } from "react";
import { useSpring, animated } from "react-spring";
import { ReactTyped } from "react-typed";
import Layout from "./Layout.js";
import Card from "./ui/card.js";
import SwitchButton from "./ui/switchButton.js";
import Vortex from "./ui/vortex.js";

import logo from "../logo.svg";

import "./Global.css";

function Home() {
  const [isListening, setIsListening] = useState(false);
  const [stream, setStream] = useState(null);

  const props = useSpring({
    to: { opacity: 1 },
    from: { opacity: 0 },
    delay: 100,
  });

  useEffect(() => {
    // Request microphone access when the component mounts
    async function requestMicrophone() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          audio: true,
        });
        setStream(stream);
      } catch (error) {
        console.error("Error accessing microphone:", error);
      }
    }
    requestMicrophone();
  }, []);

  const startJarvis = () => {
    setIsListening(true);

    // Get the selected microphone device index
    const selectedDeviceIndex = stream.getTracks()[0].getSettings().deviceId;

    fetch(
      "/run-jarvis",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          stream: stream,
          device_id: { device_index: selectedDeviceIndex },
        }),
        mode: "no-cors",
      },
    )
      .then((response) => response.text())
      .then((data) => {
        console.log("Jarvis response:", data);
        setIsListening(false);
      })
      .catch((error) => {
        console.error("Error running Jarvis:", error);
        setIsListening(false);
      });
  };

  const toggleListening = () => {
    if (isListening) {
      // Stop Jarvis
      setIsListening(false);
    } else {
      // Start Jarvis
      startJarvis();
    }
  };

  const cardData = [
    {
      title: "Open Website",
      category: "Web",
      description: "Open a website by saying 'open example.com'.",
    },
    {
      title: "Tell Time",
      category: "Time",
      description: "Ask A.L.P.H.A to tell you the current time.",
    },
    {
      title: "Check Weather",
      category: "Weather",
      description: "Get the current weather information for a city.",
    },
  ];

  return (
    <animated.div style={props}>
      <Layout>
        {/* <Vortex
          backgroundColor="black"
          rangeY={200}
          particleCount={75}
          baseHue={200}
          className="flex h-full w-full flex-col items-center justify-center"
          baseSpeed={0}
          rangeSpeed={0.5}
          baseRadius={0}
          rangeRadius={2}
        > */}
        <div className="mx-auto flex w-3/4 flex-col items-center justify-center py-10">
          {/* HEADER */}
          <h1 className="mb-10 py-2 mt-32 text-center text-3xl font-extrabold leading-none tracking-tight text-stone-50 md:text-4xl lg:text-5xl">
            I can{" "}
            <ReactTyped
              strings={["tell the time.", "schedule events.", "open websites.", "read real time data.", "change the world.", "tell you the weather."]}
              typeSpeed={50}
              loop
              backSpeed={20}
              cursorChar="✦"
              showCursor={true}
              className="inline-block bg-gradient-to-r from-pink-400 to-indigo-500 bg-clip-text text-transparent"
            />
          </h1>
          {/* END HEADER */}

          {/* BODY */}
          <p className="font-serif italic text-shadow-lg mb-16 text-center font-normal text-stone-300 shadow-black sm:px-16 lg:text-lg xl:px-48">
            A.L.P.H.A. is your cutting-edge personal intelligent assistant,
            harnessing advanced natural language processing to provide seamless,
            human-like communication and support. This powerful AI learns and
            adapts to your needs, offering personalized assistance with tasks,
            research, scheduling, smart home control, and more. Whether at home
            or on-the-go, A.L.P.H.A.'s' intuitive voice interface and continuous
            learning capabilities make it an indispensable companion,
            revolutionizing how you interact with technology. Experience the
            future of artificial intelligence tailored to your lifestyle -
            explore A.L.P.H.A. today.
          </p>
          {/* END BODY */}

          {/* BUTTON */}
          <SwitchButton
            text={isListening ? "Stop" : "Start"}
            isActive={isListening}
            onClick={toggleListening}
          />
          {/* END BUTTON */}
        </div>
        {/* </Vortex> */}

        {/* CARDS */}
        <div className="flex flex-wrap justify-center px-40">
          {cardData.map((data, index) => (
            <Card
              key={index}
              title={data.title}
              category={data.category}
              description={data.description}
              imageSrc={logo}
            />
          ))}
        </div>
        {/* END CARDS */}
        
        <div
          className="w-56 ml-4 rounded border border-blue-500/30 bg-blue-900/30 p-3 text-center ext-white duration-300 glow:border-teal-500/60 glow:bg-teal-500/40"
        >
          <p className="font-mono text-xl text-teal-300 glow:text-stone-50">
            TSA TeamID: 2237
          </p>
        </div>

      </Layout>
    </animated.div>
  );
}

export default Home;