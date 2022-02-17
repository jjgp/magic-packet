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
  const [sampleCount, setSampleCount] = useState(0);
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

  const onSampleClicked = useCallback(async () => {
    try {
      await fetchPost("sample", { data, rate: context.sampleRate });
      setSampleCount((sc) => sc + 1);
    } catch (error) {
      console.log(error);
    }
  }, [data, context.sampleRate, setSampleCount]);

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

  const samplesString = `No. Samples: ${sampleCount}`;
  const loss = status?.model_history?.loss;
  const lossString = `Loss: ${
    (loss && loss[loss.length - 1].toFixed(3)) || "..."
  }`;
  const accuracy = status?.model_history?.accuracy;
  const accuracyString = `Acc: ${
    (accuracy && accuracy[accuracy.length - 1].toFixed(3)) || "..."
  }`;
  const predictionString = `Prediction: ${"..."}`;
  const statusString = `${samplesString}, ${lossString}, ${accuracyString}, ${predictionString}`;

  return (
    <div className="App">
      <header className="App-header">
        <p>{statusString}</p>
        <canvas ref={canvasRef} width={window.innerWidth} height={300} />
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
          <button
            className="App-btn"
            disabled={!data}
            onClick={onSampleClicked}
          >
            {"Submit"}
          </button>
          <button
            className="App-btn"
            disabled={!status?.num_samples}
            onClick={() => fetchPost("train")}
          >
            {"Train"}
          </button>
          <button
            className="App-btn"
            disabled={!data || !status?.has_model}
            onClick={() => {}}
          >
            {"Infer"}
          </button>
        </div>
      </header>
    </div>
  );
};

export default App;
