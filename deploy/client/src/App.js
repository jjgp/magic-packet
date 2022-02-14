import { useCallback, useRef, useState } from "react";
import "./App.css";
import { useAnalyserRecorder } from "./hooks";
import { useUserMedia } from "./providers";

const App = () => {
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

  const onSubmitClicked = useCallback(async () => {
    /*
      TODO: submit blobs to api once it might be supported. the audioBitsPerSecond or
      sampleRate might need to be sent along  with the blob it so that the audio may
      be downsampled.
      - https://developer.mozilla.org/en-US/docs/Web/API/BaseAudioContext/sampleRate
      - https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder/audioBitsPerSecond

      TODO: this closure should be debounced so that it doesn't spam the API...
    */
    console.log(await fetch("/api"));
  }, [data]);

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
          <button
            className="App-btn"
            disabled={!data}
            onClick={onSubmitClicked}
          >
            {"Submit"}
          </button>
        </div>
      </header>
    </div>
  );
};

export default App;
