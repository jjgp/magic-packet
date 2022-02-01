/* Adapted from: https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/InputAudioContext.tsx */

import React, { createContext, useContext, useEffect, useState } from "react";
import { useCallback } from "react/cjs/react.development";
import { useUserMedia } from "./UserMedia";
import usePrevious from "../hooks/usePrevious";

const audioStreamState = (context = null, source = null) => ({
  context,
  source,
});

const AudioStreamContext = createContext(audioStreamState());

export const useAudioStream = () => useContext(AudioStreamContext);

const AudioStream = ({ children }) => {
  const [state, setState] = useState();
  const { stream } = useUserMedia();
  const previousState = usePrevious(state);

  useEffect(() => {
    if (stream) {
      const context = new (window.AudioContext || window.webkitAudioContext)();
      const source = context.createMediaStreamSource(stream);
      setState(audioStreamState(context, source));
    }
  }, [stream]);

  const cleanup = useCallback(() => {
    if (state) {
      const { context, source } = state;
      context && context.close();
      source && source.disconnect();
      setState(null);
    }
  }, [state]);

  useEffect(() => {
    if (!stream) {
      cleanup();
    }

    return () => cleanup();
  }, [cleanup, previousStream, stream]);

  return (
    <AudioStreamContext.Provider value={{ ...state }} children={children} />
  );
};

export default AudioStream;
