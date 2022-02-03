import "./App.css";
import KeywordVisualizer from "./components/KeywordVisualizer";
import { useUserMedia } from "./providers/UserMedia";

const App = () => {
  const { stream, start, stop } = useUserMedia();
  const toggleStream = () => (stream ? stop() : start());

  return (
    <div className="App">
      <header className="App-header">
        <KeywordVisualizer
          displayWidthInSeconds={3.0}
          width={window.innerWidth}
          height={300}
        />
        <button className="App-btn" onClick={toggleStream} />
      </header>
    </div>
  );
};

export default App;
