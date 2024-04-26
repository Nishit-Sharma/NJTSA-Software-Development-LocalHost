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
  const [error, setError] = useState(null);

  const props = useSpring({
    to: { opacity: 1 },
    from: { opacity: 0 },
    delay: 100,
  });

  useEffect(() => {
    // Request microphone access when the component mounts
    async function requestMicrophone() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        setStream(stream);
      } catch (error) {
        console.error("Error accessing microphone:", error);
      }
    }
    requestMicrophone();
  }, []);

  const startJarvis = () => {
    setIsListening(true);
    // Pass the stream to the Python script
    fetch("/run-jarvis", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ stream: stream }),
    })
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
      title: "Supercharged!",
      category: "Easy to use",
      description:
        "The new supercar is here, 543 cv and 140 000$. This is the best racing GT in years!",
    },
    {
      title: "Travel Diaries",
      category: "idk",
      description:
        "Explore the breathtaking landscapes of New Zealand with our latest travel blog series.",
    },
    {
      title: "Healthy Eating Made Easy",
      category: "Cool",
      description:
        "Discover delicious and nutritious recipes that will make you fall in love with healthy eating.",
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
          <h1 className="mb-10 mt-10 text-center text-3xl font-extrabold leading-none tracking-tight text-stone-100 md:text-4xl lg:text-5xl">
            {" "}
            I can{" "}
            <ReactTyped
              strings={["tell the time.", "schedule events.", "open websites."]}
              typeSpeed={50}
              loop
              backSpeed={20}
              cursorChar="✦"
              showCursor={true}
              className="inline-block bg-gradient-to-r from-purple-500/70 to-pink-200 bg-clip-text text-transparent"
            />
          </h1>
          {/* END HEADER */}

          {/* BODY */}
          <p className="text-shadow-lg mb-16 text-center font-normal text-stone-300 shadow-black sm:px-16 lg:text-lg xl:px-48">
            Jarvis AI is your cutting-edge personal intelligent assistant,
            harnessing advanced natural language processing to provide seamless,
            human-like communication and support. This powerful AI learns and
            adapts to your needs, offering personalized assistance with tasks,
            research, scheduling, smart home control, and more. Whether at home
            or on-the-go, Jarvis AI's intuitive voice interface and continuous
            learning capabilities make it an indispensable companion,
            revolutionizing how you interact with technology. Experience the
            future of artificial intelligence tailored to your lifestyle -
            explore Jarvis AI today.
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
      </Layout>
    </animated.div>
  );
}

export default Home;
