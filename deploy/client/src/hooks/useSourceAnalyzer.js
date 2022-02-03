import { useEffect, useState } from "react";
import { useAudioStreamSource } from "../providers/AudioStreamSource";

export const useSourceAnalyser = () => {
  const [analyser, setAnalyser] = useState();
  const { source } = useAudioStreamSource();

  useEffect(() => {
    if (source) {
      const analyser = source.context.createAnalyser();
      analyser.smoothingTimeConstant = 1;
      setAnalyser(analyser);
    }
  }, [source]);

  useEffect(() => {
    const cleanup = () => {
      if (analyser) {
        analyser.disconnect();
        setAnalyser(undefined);
      }
    };

    if (analyser) {
      if (source) {
        const downSampler = new AudioWorkletNode(
          source.context,
          "downSampleProcessor"
        );
        source.connect(downSampler).connect(analyser);
      } else {
        cleanup();
      }
    }

    return cleanup;
  }, [analyser, source]);

  return analyser;
};
