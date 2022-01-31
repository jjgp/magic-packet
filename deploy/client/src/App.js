import _ from "webrtc-adapter"; // shims the getUserMedia to support a wider range of browsers
import logo from "./logo.svg";
import "./App.css";

const constraints = (window.constraints = {
  audio: true,
  video: false,
});

async function getUserMedia() {
  await navigator.mediaDevices.getUserMedia(constraints);
}

async function App() {
  await getUserMedia();

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
