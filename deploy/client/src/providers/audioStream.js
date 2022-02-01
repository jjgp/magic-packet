import React, { createContext, useContext, useEffect, useState } from "react";
import { useUserMedia } from "./userMedia";

const audioStreamState = (context = null, source = null) => ({
  context,
  source,
});

const AudioStreamContext = createContext(audioStreamState());

export const useAudioStream = () => useContext(AudioStreamContext);

const AudioStream = ({ children }) => {
  const [state, setState] = useState(audioStreamState());
  const { stream } = useUserMedia();

  useEffect(() => {
    if (stream) {
      const context = new (window.AudioContext || window.webkitAudioContext)();
      const source = context.createMediaStreamSource(stream);
      setState(audioStreamState(context, source));
    }
  }, [stream]);

  const cleanup = ({ context, source }) => {
    context && context.close();
    source && source.disconnect();
  };

  useEffect(() => {
    if (!stream) {
      cleanup(state);
    }

    return () => cleanup(state);
  }, [state, stream]);

  return (
    <AudioStreamContext.Provider value={{ ...state }} children={children} />
  );
};

export default AudioStream;
