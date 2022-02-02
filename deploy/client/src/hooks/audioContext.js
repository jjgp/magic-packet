import { useEffect, useRef, useState } from "react";

export const useAudioContext = () => {
  const contextRef = useRef();
  const nodeRef = useRef();
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    contextRef.current = new (window.AudioContext ||
      window.webkitAudioContext)();
    const addModule = async () => {
      await contextRef.current.resume();
      await contextRef.current.audioWorklet.addModule(
        "worklets/downSampleProcessor.js"
      );
      nodeRef.current = new AudioWorkletNode(
        contextRef.current,
        "downSampleProcessor"
      );
      setIsReady(true);
    };

    addModule();
  });

  useEffect(
    () => () => {
      nodeRef.current.disconnect();
      contextRef.current.close();
    },
    []
  );

  return [isReady, contextRef.current];
};
