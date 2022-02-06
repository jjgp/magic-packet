import "webrtc-adapter"; // shims the AudioContext to support a wider range of browsers
import { useEffect, useRef } from "react";

export const useAudioContext = () => {
  const contextRef = useRef(new window.AudioContext());

  useEffect(
    () => () => {
      contextRef.current.close();
      contextRef.current = null;
    },
    []
  );

  return contextRef.current;
};
