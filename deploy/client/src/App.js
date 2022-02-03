import "./App.css";
import KeywordVisualizer from "./components/KeywordVisualizer";
import TFDataMicrophone from "./providers/TFDataMicrophone";

const microphoneConfig = {
  fftSize: 1024,
  columnTruncateLength: 232,
  numFramesPerSpectrogram: 43,
  includeSpectrogram: true,
  includeWaveform: true,
};

const App = () => (
  <div className="App">
    <header className="App-header">
      <TFDataMicrophone microphoneConfig={microphoneConfig}>
        <KeywordVisualizer displayWidthInSeconds={3} />
      </TFDataMicrophone>
    </header>
  </div>
);

export default App;
