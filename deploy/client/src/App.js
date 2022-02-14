import { useCallback, useRef, useState } from "react";
import "./App.css";
import { useAnalyserRecorder } from "./hooks";
import { useUserMedia } from "./providers";

const App = ({ sampleRate }) => {
  const [data, setData] = useState();
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

  const onTrainClicked = useCallback(async () => {
    const body = JSON.stringify({ data, sampleRate });

    try {
      await fetch("/api/train", {
        body,
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
      setData(null);
    } catch (error) {
      console.log(error);
    }
  }, [data, sampleRate]);

  return (
    <div className="App">
      <header className="App-header">
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
        </div>
      </header>
    </div>
  );
};

export default App;
