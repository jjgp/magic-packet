import { useEffect, useState } from "react";

export const useSourceAnalyser = (destination) => {
  const [analyser, setAnalyser] = useState();

  useEffect(() => {
    if (destination) {
      const node = destination.context.createAnalyser();
      // TODO: iterate over passed parameters and hasOwnKey
      node.smoothingTimeConstant = 1;
      setAnalyser(destination.connect(node));

      return function disconnect() {
        node.disconnect();
      };
    } else {
      setAnalyser(null);
    }
  }, [destination]);

  return analyser;
};
