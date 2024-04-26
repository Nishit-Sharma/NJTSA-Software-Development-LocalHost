const express = require("express");
const { spawn } = require("child_process");

const app = express();
const port = 3001;

app.use(express.json());

// This is what home.js calls to run the server
app.post("/run-jarvis", (req, res) => {
  console.log("Received request to run Jarvis");

  // Get the stream data from the request body
  const { stream } = req.body;

  // Run the Jarvis Python script and pass the stream data
  const jarvisProcess = spawn("python", ["./src/components/jarvis.py", JSON.stringify(stream)]);

  jarvisProcess.stdout.on("data", (data) => {
    console.log(`Jarvis: ${data}`);
    // Send the data from the Python script back to the client
    res.write(data.toString());
  });

  jarvisProcess.stderr.on("data", (data) => {
    console.error(`Jarvis error: ${data}`);
    // Send the error data from the Python script back to the client
    res.write(`Jarvis error: ${data.toString()}`);
  });

  jarvisProcess.on("close", (code) => {
    console.log(`Jarvis process exited with code ${code}`);
    // End the response
    res.end();
  });
});

// Add a default route
app.get("/", (req, res) => {
  res.send("Server is running");
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});