import { useEffect, useRef, useState } from "react";

export const useAudioContext = ({ modules }) => {
  const contextRef = useRef();
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    contextRef.current = new (window.AudioContext ||
      window.webkitAudioContext)();
    const addModule = async () => {
      await contextRef.current.resume();
      await Promise.all(
        modules.map(async (module) => {
          await contextRef.current.audioWorklet.addModule(module);
        })
      );
      setIsReady(true);
    };

    addModule();
  }, [modules]);

  useEffect(
    () => () => {
      contextRef.current.close();
      contextRef.current = null;
    },
    []
  );

  return [isReady, contextRef.current];
};
