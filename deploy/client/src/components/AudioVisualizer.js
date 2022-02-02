/*
  Adapted from:
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/AudioAnalyserContext.tsx
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/AudioVisualizer.tsx
*/

import React, { createRef, useEffect, useState } from "react";
import { useAudioStreamSource } from "../providers/AudioStreamSource";

const useSourceAnalyser = () => {
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
        source.connect(analyser);
      } else {
        cleanup();
      }
    }

    return cleanup;
  }, [analyser, source]);

  return analyser;
};

const AudioVisualizer = ({ displaySeconds, ...props }) => {
  const analyser = useSourceAnalyser();
  const canvasRef = createRef();
  const slicePosRef = createRef(0);

  useEffect(() => {
    // TODO: clear rect on toggle of microphone
    if (!analyser) {
      return;
    }

    let animationFrame;
    const data = new Uint8Array(analyser.frequencyBinCount);
    const sampleRate = analyser.context.sampleRate;

    const draw = () => {
      analyser.getByteTimeDomainData(data);
      const canvas = canvasRef.current;
      if (canvas) {
        const context = canvas.getContext("2d");
        const { height, width } = canvas;
        let x = slicePosRef.current;
        const sliceWidth = width / (sampleRate * displaySeconds);
        const dataWidth = sliceWidth * 2 * data.length;

        if (context) {
          context.lineWidth = 2;
          context.strokeStyle = "#fff";
          if (x + dataWidth < width) {
            context.clearRect(x, 0, dataWidth, height);
          } else {
            context.clearRect(x, 0, width, height);
            context.clearRect(0, 0, dataWidth - (width - x), height);
          }

          context.beginPath();
          context.moveTo(x, height / 2);
          for (const item of data) {
            const y = (item / 255.0) * height;
            context.lineTo(x, y);
            x += sliceWidth;
            if (x > width) {
              context.lineTo(width, height / 2);
              context.moveTo(0, height / 2);
            }
            x %= width;
          }
          context.lineTo(x, height / 2);
          context.stroke();
          slicePosRef.current = x;
        }
      }
      animationFrame = requestAnimationFrame(draw);
    };
    draw();

    return () => {
      cancelAnimationFrame(animationFrame);
    };
  }, [analyser, canvasRef, displaySeconds, slicePosRef]);

  return <canvas ref={canvasRef} {...props} />;
};

export default AudioVisualizer;
