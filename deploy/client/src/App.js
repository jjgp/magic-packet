import { useRef } from "react";
import "./App.css";
import { useAudioVisualizer } from "./hooks";
import { useAudioStreamSource, useUserMedia } from "./providers";

const App = () => {
  const canvasRef = useRef();
  const { stream, start, stop } = useUserMedia();
  const { source } = useAudioStreamSource();

  useAudioVisualizer(source, canvasRef);

  const toggleStream = () => (stream ? stop() : start());

  return (
    <div className="App">
      <header className="App-header">
        <canvas ref={canvasRef} width={window.innerWidth} height={300} />
        <div className="App-btns">
          <button className="App-btn" onClick={toggleStream}>
            {stream ? "Stop Record" : "Record"}
          </button>
          <button className="App-btn" onClick={toggleStream}>
            {stream ? "Submit" : "Submit"}
          </button>
        </div>
      </header>
    </div>
  );
};

export default App;
