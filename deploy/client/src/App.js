import { useRef } from "react";
import "./App.css";
import { useAnalyserRecorder } from "./hooks";
import { useAudioStreamSource, useUserMedia } from "./providers";

const App = () => {
  const canvasRef = useRef();
  const { start, stop } = useUserMedia();
  const { source } = useAudioStreamSource();

  const onSecondsEnd = (timeDomainData) => {
    stop();
  };

  useAnalyserRecorder(source, canvasRef, { numberOfSeconds: 1, onSecondsEnd });

  const submit = async () => {
    /*
      TODO: submit blobs to api once it might be supported. the audioBitsPerSecond or
      sampleRate might need to be sent along  with the blob it so that the audio may
      be downsampled.
      - https://developer.mozilla.org/en-US/docs/Web/API/BaseAudioContext/sampleRate
      - https://developer.mozilla.org/en-US/docs/Web/API/MediaRecorder/audioBitsPerSecond

      TODO: this closure should be debounced so that it doesn't spam the API...
    */
    console.log(await fetch("/api"));
  };

  return (
    <div className="App">
      <header className="App-header">
        <canvas ref={canvasRef} width={window.innerWidth} height={300} />
        <div className="App-btns">
          <button className="App-btn" disabled={source} onClick={start}>
            {"Record"}
          </button>
          <button className="App-btn" onClick={submit}>
            {"Submit"}
          </button>
        </div>
      </header>
    </div>
  );
};

export default App;
