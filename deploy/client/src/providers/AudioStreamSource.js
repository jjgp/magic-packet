/* Adapted from: https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/InputAudioContext.tsx */

import React, {
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";
import { useUserMedia } from "./UserMedia";

const AudioStreamSourceContext = createContext({ source: null });

export const useAudioStreamSource = () => useContext(AudioStreamSourceContext);

const AudioStreamSource = ({ children }) => {
  const contextRef = useRef();
  const [source, setSource] = useState();
  const { stream } = useUserMedia();

  useEffect(() => {
    if (stream && !source) {
      if (!contextRef.current) {
        contextRef.current = new (window.AudioContext ||
          window.webkitAudioContext)();
      }
      setSource(contextRef.current.createMediaStreamSource(stream));
    } else if (!stream && source) {
      setSource(null);
    }
  }, [source, stream]);

  useEffect(() => () => source && source.disconnect(), [source]);

  useEffect(
    () => async () => {
      contextRef.current && (await contextRef.current.close());
      contextRef.current = null;
    },
    []
  );

  return (
    <AudioStreamSourceContext.Provider value={{ source }} children={children} />
  );
};

export default AudioStreamSource;
