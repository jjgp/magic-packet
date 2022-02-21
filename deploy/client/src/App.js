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
  const [status, setStatus] = useState("");
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
    setPrediction(null);
    start();
  }, [start]);

  const onPredictClick = useCallback(async () => {
    setStatus("predict");
    setPrediction(null);
    try {
      const response = await fetchPost("predict", {
        data,
        rate: context.sampleRate,
      });
      if (response.ok) {
        const responseJson = await response.json();
        console.log(responseJson?.prediction);
        setPrediction(responseJson?.prediction);
      } else console.log(response);
    } catch (error) {
      console.log(error);
    }
    setStatus("");
  }, [data, context.sampleRate]);

  const onSampleClicked = useCallback(async () => {
    setStatus("sample");
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
    setStatus("");
  }, [data, context.sampleRate]);

  const onTrainClicked = async () => {
    setStatus("train");
    try {
      const response = await fetch("/api/train");
      if (response.ok) setHistory(await response.json());
      else console.log(response);
    } catch (error) {
      console.log(error);
    }
    setStatus(false);
  };

  useEffect(
    () => fetch("/api/reset", { method: "POST" }).catch(console.log),
    []
  );

  let statusString = "";
  if (prediction) {
    const predictionString = ["silence", "unknown word", "wake word"][
      prediction.indexOf(Math.max(...prediction))
    ];
    statusString = `Audio contains ${predictionString}`;
  } else if (status === "train") {
    statusString = "Training...";
  } else if (!history && sampleCount) {
    statusString = `No. Samples: ${sampleCount}`;
  }

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
              disabled={status || !data}
              onClick={onSampleClicked}
            >
              {"Submit"}
            </button>
          )}
          {!history && (
            <button
              className="App-btn"
              disabled={status || sampleCount < 1}
              onClick={onTrainClicked}
            >
              {"Train"}
            </button>
          )}
          {history && (
            <button
              className="App-btn"
              disabled={status}
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
