/*
  Adapted from:
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/AudioAnalyserContext.tsx
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/AudioVisualizer.tsx
*/

import React, { createRef, useEffect } from "react";
import { useAudioWorklet, useSourceAnalyser } from "../hooks";
import { useAudioStreamSource } from "../providers/AudioStreamSource";

function averageInterpolate(input, outputLength) {
  const output = [];
  const accumulateRange = Math.floor(input.length / outputLength);
  for (let i = 0; i < outputLength - 1; ++i) {
    let acc = 0,
      start = i * accumulateRange;
    for (let j = start; j < start + accumulateRange; ++j) {
      acc += input[j];
    }
    output[i] = acc / accumulateRange;
  }
  return output;
}

function linearInterpolate(input, outputLength) {
  // linear downsampling adapted from: https://stackoverflow.com/a/27437245
  const output = [];
  output[0] = input[0]; // keep start value
  // the distance between sampled values
  const skipDistance = (input.length - 1) / (outputLength - 1);
  for (let i = 1; i < outputLength - 1; ++i) {
    const pos = i * skipDistance;
    const i0 = Math.floor(pos);
    const i1 = Math.ceil(pos);
    // linearly interpolate input between indices i0 and i1
    output[i] = input[i0] + (pos - i0) * (input[i1] - input[i0]);
  }
  output[outputLength - 1] = input[input.length - 1]; // keep end value
  return output;
}

const KeywordVisualizer = ({
  displayWidthInSeconds,
  fftSize = 2048, // NOTE: in howl it's 256
  smoothingTimeConstant = 0.2,
  ...props
}) => {
  const { source } = useAudioStreamSource();
  const _ = useAudioWorklet("downsampleProcessor", source);
  const analyser = useSourceAnalyser(source, {
    fftSize,
    smoothingTimeConstant,
  });
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

    let animationFrame;
    const analyzed = new Uint8Array(analyser.frequencyBinCount);
    const sampleRate = analyser.context.sampleRate;
    const sliceWidth = 2;
    const sampleLength =
      (analyser.frequencyBinCount * width) /
      (sampleRate * displayWidthInSeconds);

    const draw = () => {
      animationFrame = requestAnimationFrame(draw);

      analyser.getByteTimeDomainData(analyzed);
      let data = analyzed.slice();
      data = linearInterpolate(data, Math.floor(sampleLength / 2));

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
        if (x > width - 1) {
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
  }, [analyser, canvasRef, displayWidthInSeconds, slicePosRef]);

  return <canvas ref={canvasRef} {...props} />;
};

export default KeywordVisualizer;
