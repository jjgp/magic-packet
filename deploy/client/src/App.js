import { useRef } from "react";
import "./App.css";
import { useAudioVisualizer, useMediaRecorder } from "./hooks";
import { useAudioStreamSource, useUserMedia } from "./providers";

const App = () => {
  const canvasRef = useRef();
  const { stream, start, stop: stopStream } = useUserMedia();
  const { blob, stop: stopRecorder } = useMediaRecorder(stream);
  const { source } = useAudioStreamSource();
  useAudioVisualizer(source, canvasRef, { displaySeconds: 1 });

  const canSubmit = !stream && blob && blob.size;

  const stop = () => {
    stopRecorder();
    stopStream();
  };

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

  const toggleStream = () => (stream ? stop() : start());

  return (
    <div className="App">
      <header className="App-header">
        <canvas ref={canvasRef} width={window.innerWidth} height={300} />
        <div className="App-btns">
          <button className="App-btn" onClick={toggleStream}>
            {stream ? "Stop Record" : "Record"}
          </button>
          <button className="App-btn" disabled={!canSubmit} onClick={submit}>
            {"Submit"}
          </button>
        </div>
      </header>
    </div>
  );
};

export default App;
