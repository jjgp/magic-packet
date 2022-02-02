import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import AudioStreamSource from "./providers/AudioStreamSource";
import UserMedia from "./providers/UserMedia";

const Root = () => {
  const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  const constraints = { audio: true, video: false };
  return (
    <React.StrictMode>
      <UserMedia mediaStreamConstraints={constraints}>
        <AudioStreamSource context={audioCtx}>
          <App />
        </AudioStreamSource>
      </UserMedia>
    </React.StrictMode>
  );
};

ReactDOM.render(<Root />, document.getElementById("root"));

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
