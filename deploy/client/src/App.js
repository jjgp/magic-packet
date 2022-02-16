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

const App = ({ context }) => {
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
      setData(timeDomainData.map((byte) => byte / 128 - 1));
      stop();
    },
    [stop]
  );

  useAnalyserRecorder(canvasRef, { numberOfSeconds: 1, onSecondsEnd });

  const onPlayClicked = useCallback(() => {
    const buffer = context.createBuffer(1, data.length, context.sampleRate);
    const buffering = buffer.getChannelData(0);
    data.forEach((value, index) => (buffering[index] = value));

    const source = context.createBufferSource();
    source.buffer = buffer;
    source.connect(context.destination);
    source.start(0);
  }, [context, data]);

  const onSampleClicked = usePostSample(
    "sample",
    { data, rate: context.sampleRate },
    setData
  );

  const onInferClicked = usePostSample(
    "infer",
    { data, rate: context.sampleRate },
    setData
  );

  useEffect(() => {
    // fetch("/api/reset", { method: "POST" }).catch(console.log);
    // setInterval(async () => {
    //   try {
    //     const response = await fetch("/api/poll");
    //     setStatus(await response.json());
    //   } catch (error) {
    //     console.log(error);
    //   }
    // }, 2000);
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
          <button className="App-btn" disabled={!data} onClick={onPlayClicked}>
            {"Play"}
          </button>
          <button
            className="App-btn"
            disabled={!data}
            onClick={onSampleClicked}
          >
            {"Sample"}
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
