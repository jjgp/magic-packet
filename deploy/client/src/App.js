import { useCallback, useEffect, useRef, useState } from "react";
import "./App.css";
import { useAnalyserRecorder } from "./hooks";
import { useUserMedia } from "./providers";

const postBody = (path, body) =>
  fetch(`/api/${path}`, {
    body: JSON.stringify(body),
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

const usePostSample = (path, body, setData) =>
  useCallback(async () => {
    try {
      await postBody(path, body);
      setData(null);
    } catch (error) {
      console.log(error);
    }
  }, [path, body, setData]);

const App = ({ sampleRate }) => {
  const [data, setData] = useState();
  const [status, setStatus] = useState();
  const canvasRef = useRef();
  const { stream, start, stop } = useUserMedia();

  const onRecordClick = useCallback(() => {
    setData(null);
    start();
  }, [start]);

  const onSecondsEnd = useCallback(
    (timeDomainData) => {
      setData(timeDomainData);
      stop();
    },
    [stop]
  );

  useAnalyserRecorder(canvasRef, { numberOfSeconds: 1, onSecondsEnd });

  const onTrainClicked = usePostSample("train", { data, sampleRate }, setData);
  const onInferClicked = usePostSample("infer", { data, sampleRate }, setData);

  useEffect(() => {
    fetch("/api/reset", { method: "POST" }).catch(console.log);
    setInterval(async () => {
      try {
        const response = await fetch("/api/poll");
        setStatus(await response.json());
      } catch (error) {
        console.log(error);
      }
    }, 2000);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p>{status}</p>
        <canvas ref={canvasRef} width={window.innerWidth} height={300} />
        <div className="App-btns">
          <button
            className="App-btn"
            disabled={stream && stream.active}
            onClick={onRecordClick}
          >
            {"Record"}
          </button>
          <button className="App-btn" disabled={!data} onClick={onTrainClicked}>
            {"Train"}
          </button>
          <button className="App-btn" disabled={!data} onClick={onInferClicked}>
            {"Infer"}
          </button>
        </div>
      </header>
    </div>
  );
};

export default App;
