/*
  Adapted from:
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/AudioAnalyserContext.tsx
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/AudioVisualizer.tsx
*/

import React, { useEffect, useRef } from "react";
import { useSourceAnalyser } from "../hooks";
import { useAudioStreamSource } from "../providers/AudioStreamSource";

function sampleMaxAmplitudes(input, outputLength) {
  const output = [];
  const sampleWidth = Math.floor(input.length / outputLength);
  for (let i = 0; i < outputLength - 1; ++i) {
    const start = i * sampleWidth;
    let max = -Infinity,
      min = Infinity;
    for (let j = i * sampleWidth; j < start + sampleWidth; ++j) {
      max = Math.max(max, input[j]);
      min = Math.min(min, input[j]);
    }
    output[i] = max - min;
  }
  return output;
}

const KeywordVisualizer = ({
  displayWidthInSeconds = 3,
  smoothingTimeConstant = 1,
  ...props
}) => {
  const { source } = useAudioStreamSource();
  const analyser = useSourceAnalyser(source, { smoothingTimeConstant });
  const canvasRef = useRef();
  const drawXRef = useRef(0);

  useEffect(() => {
    if (!analyser || !canvasRef.current) {
      return;
    }

    const canvas = canvasRef.current;
    const { height, width } = canvas;

    const context = canvas.getContext("2d");
    context.lineWidth = 2;
    context.strokeStyle = "#fff";

    const midHeight = height / 2;

    const timeData = new Uint8Array(analyser.fftSize);
    const sampleRate = analyser.context.sampleRate;
    const sliceWidth = 2;
    const sampleLength =
      (analyser.frequencyBinCount * width) /
      (sampleRate * displayWidthInSeconds);

    const draw = () => {
      analyser.getByteTimeDomainData(timeData);
      const amplitudes = sampleMaxAmplitudes(
        timeData.slice(),
        Math.floor(sampleLength / 2)
      );

      let x = drawXRef.current;
      const drawWidth = amplitudes.length * sliceWidth + 2 * sliceWidth;

      if (x + drawWidth < width) {
        context.clearRect(Math.floor(x), 0, Math.ceil(drawWidth), height);
      } else {
        context.clearRect(x, 0, width, height);
        context.clearRect(0, 0, drawWidth - (width - x), height);
      }

      context.beginPath();
      for (const item of amplitudes) {
        const y = (item / 255.0) * height;
        context.moveTo(x, midHeight - y / 2);
        context.lineTo(x, midHeight + y / 2);
        x += sliceWidth;
        if (x > width - 1) {
          context.moveTo(0, midHeight);
        }
        x %= width;
      }
      context.lineTo(x, midHeight);
      context.stroke();
      drawXRef.current = x;
    };

    let animationFrame;
    const render = (timestamp) => {
      draw();
      animationFrame = requestAnimationFrame(render);
    };
    animationFrame = requestAnimationFrame(render);

    return () => {
      cancelAnimationFrame(animationFrame);
    };
  }, [analyser, canvasRef, displayWidthInSeconds, drawXRef]);

  return <canvas ref={canvasRef} {...props} />;
};

export default KeywordVisualizer;
