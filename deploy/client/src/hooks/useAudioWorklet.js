import { useEffect, useState } from "react";

export const useAudioWorklet = (name, destination) => {
  const [worklet, setWorklet] = useState();

  useEffect(() => {
    if (destination) {
      const node = new AudioWorkletNode(destination.context, name);
      setWorklet(destination.connect(node));

      return function disconnect() {
        node.disconnect();
      };
    } else {
      setWorklet(null);
    }
  }, [name, destination]);

  return worklet;
};
