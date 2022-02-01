import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import AudioStream from "./providers/AudioStream";
import UserMedia from "./providers/UserMedia";

ReactDOM.render(
  <React.StrictMode>
    <UserMedia mediaStreamConstraints={{ audio: true, video: false }}>
      <AudioStream>
        <App />
      </AudioStream>
    </UserMedia>
  </React.StrictMode>,
  document.getElementById("root")
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
