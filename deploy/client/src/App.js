import { useCallback, useEffect, useRef, useState } from "react";
import "./App.css";
import { useAnalyserRecorder } from "./hooks";
import { useUserMedia } from "./providers";

const fetchPost = (path, body) =>
  fetch(`/api/${path}`, {
    body: body && JSON.stringify(body),
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  });

const App = ({ context }) => {
  const [data, setData] = useState();
  const [history, setHistory] = useState();
  const [isBusy, setIsBusy] = useState(false);
  const [prediction, setPrediction] = useState();
  const [sampleCount, setSampleCount] = useState(0);
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

  const onPredictClick = useCallback(async () => {
    setIsBusy(true);
    setPrediction(null);
    try {
      const response = await fetchPost("predict", {
        data,
        rate: context.sampleRate,
      });
      if (response.ok) {
        setPrediction((await response.json())?.prediction);
      } else console.log(response);
    } catch (error) {
      console.log(error);
    }
    setIsBusy(false);
  }, [data, context.sampleRate]);

  const onSampleClicked = useCallback(async () => {
    setIsBusy(true);
    try {
      const response = await fetchPost("sample", {
        data,
        rate: context.sampleRate,
      });
      if (response.ok) setSampleCount((sc) => sc + 1);
      else console.log(response);
    } catch (error) {
      console.log(error);
    }
    setIsBusy(false);
  }, [data, context.sampleRate]);

  const onTrainClicked = async () => {
    setIsBusy(true);
    try {
      const response = await fetch("/api/train");
      if (response.ok) setHistory(await response.json());
      else console.log(response);
    } catch (error) {
      console.log(error);
    }
    setIsBusy(false);
  };

  useEffect(
    () => fetch("/api/reset", { method: "POST" }).catch(console.log),
    []
  );

  let statusString = "";
  if (sampleCount) {
    statusString = `No. Samples: ${sampleCount}`;
  }

  const pred =
    (prediction &&
      JSON.stringify(prediction?.map((value) => value.toFixed(3)))) ||
    "...";

  return (
    <div className="App">
      <header className="App-header">
        <div className="App-status">
          <pre>{statusString}</pre>
        </div>
        <canvas ref={canvasRef} width={window.innerWidth - 50} height={250} />
        <div className="App-btns">
          <button
            className="App-btn"
            disabled={stream?.active}
            onClick={onRecordClick}
          >
            {"Record"}
          </button>
          <button className="App-btn" disabled={!data} onClick={onPlayClicked}>
            {"Play"}
          </button>
          {!history && (
            <button
              className="App-btn"
              disabled={isBusy || !data}
              onClick={onSampleClicked}
            >
              {"Submit"}
            </button>
          )}
          {!history && (
            <button
              className="App-btn"
              disabled={isBusy || sampleCount < 1}
              onClick={onTrainClicked}
            >
              {"Train"}
            </button>
          )}
          {history && (
            <button
              className="App-btn"
              disabled={isBusy}
              onClick={onPredictClick}
            >
              {"Predict"}
            </button>
          )}
        </div>
      </header>
    </div>
  );
};

export default App;
