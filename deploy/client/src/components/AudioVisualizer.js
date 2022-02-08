/*
  Adapted from:
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/AudioAnalyserContext.tsx
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/AudioVisualizer.tsx
*/

import React, { useEffect, useRef } from "react";
import { useSourceAnalyser, useByteTimeDomainDataRef } from "../hooks";
import { useAudioStreamSource } from "../providers/AudioStreamSource";

function sampleMaxAmplitudes(input, outputLength) {
  const output = [];
  const sampleWidth = Math.floor(input.length / outputLength);
  for (let i = 0; i < outputLength; ++i) {
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

const AudioVisualizer = ({
  amplitudeSpacing = 3,
  amplitudeWidth = 2,
  displayWidthInSeconds = 3,
  strokeStyle = "#fff",
  ...props
}) => {
  const { source } = useAudioStreamSource();
  const analyser = useSourceAnalyser(source);
  const byteTimeDomainDataRef = useByteTimeDomainDataRef(
    analyser,
    displayWidthInSeconds
  );
  const canvasRef = useRef();

  useEffect(() => {
    const draw = () => {
      if (!byteTimeDomainDataRef.current) {
        return;
      }

      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      ctx.lineWidth = amplitudeWidth;
      ctx.strokeStyle = strokeStyle;

      const { height, width } = canvas;
      const midHeight = height / 2;

      const amplitudes = sampleMaxAmplitudes(
        byteTimeDomainDataRef.current,
        width / (amplitudeSpacing + amplitudeWidth)
      );

      let x = 0;
      ctx.clearRect(0, 0, width, height);
      ctx.beginPath();
      for (const amplitude of amplitudes) {
        const y = Math.max(2, (amplitude / 255.0) * height);
        ctx.moveTo(x, midHeight - y / 2);
        ctx.lineTo(x, midHeight + y / 2);
        x += amplitudeSpacing + amplitudeWidth;
      }
      ctx.stroke();
    };

    let animationFrame;
    const render = () => {
      draw();
      animationFrame = requestAnimationFrame(render);
    };
    render();

    return () => {
      cancelAnimationFrame(animationFrame);
    };
  }, [
    amplitudeSpacing,
    amplitudeWidth,
    byteTimeDomainDataRef,
    canvasRef,
    strokeStyle,
  ]);

  return <canvas ref={canvasRef} {...props} />;
};

export default AudioVisualizer;
