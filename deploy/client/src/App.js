import "./App.css";
import AudioVisualizer from "./components/AudioVisualizer";
import { useUserMedia } from "./providers/UserMedia";

const App = () => {
  const { stream, start, stop } = useUserMedia();
  const toggleMic = () => (stream ? stop() : start());

  return (
    <div className="App">
      <header className="App-header">
        <button className="App-btn" onClick={toggleMic}>
          {stream ? "Close Microphone" : "Open Microphone"}
        </button>
        <AudioVisualizer width={window.innerWidth} height={300} />
      </header>
    </div>
  );
};

export default App;
