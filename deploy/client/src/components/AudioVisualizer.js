/*
  Adapted from:
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/AudioAnalyserContext.tsx
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/AudioVisualizer.tsx
*/

import React, { createRef, useEffect, useState } from "react";
import { useAudioStream } from "../providers/AudioStream";

const useSourceAnalyser = () => {
  const [analyser, setAnalyser] = useState();
  const { source } = useAudioStream();

  useEffect(() => {
    if (source) {
      const analyser = source.context.createAnalyser();
      analyser.smoothingTimeConstant = 1;
      source.connect(analyser);
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
        source.connect(analyser);
      } else {
        cleanup();
      }
    }

    return cleanup;
  }, [analyser, source]);

  return analyser;
};

const AudioVisualizer = () => {
  const analyser = useSourceAnalyser();
  const canvasRef = createRef();

  useEffect(() => {
    if (!analyser) {
      return;
    }

    let raf;
    const data = new Uint8Array(analyser.frequencyBinCount);

    const draw = () => {
      raf = requestAnimationFrame(draw);
      analyser.getByteTimeDomainData(data);
      const canvas = canvasRef.current;
      if (canvas) {
        const { height, width } = canvas;
        const context = canvas.getContext("2d");
        let x = 0;
        const sliceWidth = (width * 1.0) / data.length;

        if (context) {
          context.lineWidth = 2;
          context.strokeStyle = "#fff";
          context.clearRect(0, 0, width, height);

          context.beginPath();
          context.moveTo(0, height / 2);
          for (const item of data) {
            const y = (item / 255.0) * height;
            context.lineTo(x, y);
            x += sliceWidth;
          }
          context.lineTo(x, height / 2);
          context.stroke();
        }
      }
    };
    draw();

    return () => {
      cancelAnimationFrame(raf);
    };
  }, [canvasRef, analyser]);

  return analyser ? <canvas width="600" height="300" ref={canvasRef} /> : null;
};

export default AudioVisualizer;
