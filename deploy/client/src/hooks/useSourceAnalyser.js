import { useEffect, useState } from "react";

export const useSourceAnalyser = (
  destination,
  { fftSize, smoothingTimeConstant }
) => {
  const [analyser, setAnalyser] = useState();

  useEffect(() => {
    if (destination) {
      const node = destination.context.createAnalyser();
      node.smoothingTimeConstant = smoothingTimeConstant;

      setAnalyser(destination.connect(node));
      return function disconnect() {
        node.disconnect();
      };
    } else {
      setAnalyser(null);
    }
  }, [destination, fftSize, smoothingTimeConstant]);

  return analyser;
};
