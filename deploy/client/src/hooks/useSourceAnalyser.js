import { useEffect, useState } from "react";

export const useSourceAnalyser = (
  destination,
  { fftSize, smoothingTimeConstant } = {
    fftSize: 2048,
    smoothingTimeConstant: 0,
  }
) => {
  const [analyser, setAnalyser] = useState();

  useEffect(() => {
    if (destination) {
      const node = destination.context.createAnalyser();
      node.fftSize = fftSize;
      node.smoothingTimeConstant = smoothingTimeConstant;

      setAnalyser(destination.connect(node));
      return function () {
        node.disconnect();
      };
    } else {
      setAnalyser(null);
    }
  }, [destination, fftSize, smoothingTimeConstant]);

  return analyser;
};
