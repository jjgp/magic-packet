/*
  Adapted from:
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/AudioAnalyserContext.tsx
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/AudioVisualizer.tsx
*/

import React, { createRef, useEffect } from "react";
import { useSourceAnalyser } from "../hooks/useSourceAnalyzer";

const AudioVisualizer = ({ displaySeconds, ...props }) => {
  const analyser = useSourceAnalyser();
  const canvasRef = createRef();
  const slicePosRef = createRef(0);

  useEffect(() => {
    if (!analyser) {
      return;
    }

    const canvas = canvasRef.current;
    if (!canvas) {
      return;
    }
    const { height, width } = canvas;

    const context = canvas.getContext("2d");
    context.lineWidth = 2;
    context.strokeStyle = "#fff";
    context.clearRect(0, 0, width, height);

    let animationFrame;
    const data = new Uint8Array(analyser.frequencyBinCount);
    const sampleRate = analyser.context.sampleRate;
    const sliceWidth = width / (sampleRate * displaySeconds);

    const draw = () => {
      animationFrame = requestAnimationFrame(draw);

      analyser.getByteTimeDomainData(data);

      let x = slicePosRef.current;
      const drawWidth = data.length * sliceWidth + 2 * sliceWidth;

      if (x + drawWidth < width) {
        context.clearRect(Math.floor(x), 0, Math.ceil(drawWidth), height);
      } else {
        context.clearRect(x, 0, width, height);
        context.clearRect(0, 0, drawWidth - (width - x), height);
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
    };
    draw();

    return () => {
      cancelAnimationFrame(animationFrame);
    };
  }, [analyser, canvasRef, displaySeconds, slicePosRef]);

  return <canvas ref={canvasRef} {...props} />;
};

export default AudioVisualizer;
