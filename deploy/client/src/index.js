import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { AudioStreamSource, UserMedia } from "./providers";
import { useAudioContext } from "./hooks";

const Root = () => {
  const constraints = { audio: true, video: false };
  const audioCtx = useAudioContext();

  return (
    <React.StrictMode>
      <UserMedia mediaStreamConstraints={constraints}>
        <AudioStreamSource context={audioCtx}>
          <App context={audioCtx} />
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
