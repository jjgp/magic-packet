/* Adapted from: https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/InputAudioContext.tsx */

import React, { createContext, useContext, useEffect, useState } from "react";
import { useUserMedia } from "./UserMedia";

const AudioStreamSourceContext = createContext({ source: null });

export const useAudioStreamSource = () => useContext(AudioStreamSourceContext);

const AudioStreamSource = ({ children, context }) => {
  const [source, setSource] = useState();
  const { stream } = useUserMedia();

  useEffect(() => {
    if (stream) {
      setSource(context.createMediaStreamSource(stream));
    } else {
      setSource(null);
    }
  }, [context, stream]);

  useEffect(() => () => source && source.disconnect(), [source]);

  return (
    <AudioStreamSourceContext.Provider value={{ source }} children={children} />
  );
};

export default AudioStreamSource;
