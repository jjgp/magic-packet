import { useEffect, useRef } from "react";
import "./App.css";
import { useAudioVisualizer, useMediaRecorder } from "./hooks";
import { useAudioStreamSource, useUserMedia } from "./providers";

const App = () => {
  const canvasRef = useRef();
  const { stream, start, stop: stopStream } = useUserMedia();
  const { blob, stop: stopRecorder } = useMediaRecorder(stream);
  const { source } = useAudioStreamSource();
  useAudioVisualizer(source, canvasRef);

  const stop = () => {
    stopRecorder();
    stopStream();
  };

  const toggleStream = () => (stream ? stop() : start());
  const canSubmit = !stream && blob && blob.size;

  useEffect(() => {
    (async () => console.log(await fetch("/api")))();
  });

  return (
    <div className="App">
      <header className="App-header">
        <canvas ref={canvasRef} width={window.innerWidth} height={300} />
        <div className="App-btns">
          <button className="App-btn" onClick={toggleStream}>
            {stream ? "Stop Record" : "Record"}
          </button>
          <button className="App-btn" disabled={!canSubmit}>
            {"Submit"}
          </button>
        </div>
      </header>
    </div>
  );
};

export default App;
