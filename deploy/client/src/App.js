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

const App = ({ context }) => {
  const [data, setData] = useState();
  const [status, setStatus] = useState();
  const canvasRef = useRef();
  const { stream, start, stop } = useUserMedia();

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

  const onRecordClick = useCallback(() => {
    setData(null);
    start();
  }, [start]);

  const usePostSample = (path) =>
    useCallback(async () => {
      try {
        await postBody(path, { data, rate: context.sampleRate });
        setData(null);
      } catch (error) {
        console.log(error);
      }
    }, [path, data, context.sampleRate, setData]);

  const onSampleClicked = usePostSample("sample");

  const onInferClicked = usePostSample("infer");

  useEffect(() => {
    fetch("/api/reset", { method: "POST" }).catch(console.log);

    const intervalID = setInterval(async () => {
      try {
        const response = await fetch("/api/poll");
        setStatus(await response.json());
      } catch (error) {
        console.log(error);
      }
    }, 3000);

    return () => clearInterval(intervalID);
  }, []);

  const statusString = `Nº Samples: ${status?.num_samples || 0}`;

  return (
    <div className="App">
      <header className="App-header">
        <p>{statusString}</p>
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
            {"Submit"}
          </button>
          <button className="App-btn" disabled={!status || !status.num_samples}>
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
