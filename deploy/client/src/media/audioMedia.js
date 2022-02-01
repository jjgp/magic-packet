import React, { createContext, useContext, useEffect, useState } from "react";
import { useMediaStream } from "./userMedia";

const audioMediaState = (audioContext = null, audioSource = null) => ({
  audioContext,
  audioSource,
});

const AudioMediaContext = createContext(audioMediaState());

export const useAudioSource = () => useContext(AudioMediaContext);

const AudioMedia = ({ children }) => {
  const [state, setState] = useState(audioMediaState());
  const { stream } = useMediaStream();

  useEffect(() => {
    if (stream) {
      const audioContext = new (window.AudioContext ||
        window.webkitAudioContext)();
      const audioSource = audioContext.createMediaStreamSource(stream);
      setState(audioMediaState(audioContext, audioSource));
    }
  }, [stream]);

  const cleanup = ({ audioContext, audioSource }) => {
    audioContext && audioContext.close();
    audioSource && audioSource.disconnect();
  };

  useEffect(() => {
    if (!stream) {
      cleanup(state);
    }

    return () => cleanup(state);
  }, [state, stream]);

  return (
    <AudioMediaContext.Provider value={{ ...state }} children={children} />
  );
};

export default AudioMedia;
