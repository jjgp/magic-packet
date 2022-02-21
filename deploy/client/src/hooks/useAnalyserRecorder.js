/*
  Adapted from:
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/AudioAnalyserContext.tsx
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/AudioVisualizer.tsx
*/

import { useEffect, useRef } from "react";
import { useSourceAnalyser } from ".";
import { useAudioStreamSource } from "../providers";

function resampleMaxAmplitudes(input, outputLength) {
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

export const useAnalyserRecorder = (canvasRef, parameters) => {
  const {
    amplitudeSpacing = 4,
    amplitudeWidth = 3,
    numberOfSeconds = 1,
    onSecondsEnd = () => {},
    strokeStyle = "#272d2d",
  } = parameters;
  const { source } = useAudioStreamSource();
  const analyser = useSourceAnalyser(source);
  const amplitudesRef = useRef();
  const timeDataRef = useRef();

  useEffect(() => {
    if (analyser) {
      amplitudesRef.current = [];
      timeDataRef.current = [];

      const fftSize = analyser.fftSize;
      const sampleRate = analyser.context.sampleRate;
      const totalSamples = numberOfSeconds * sampleRate;
      const width = canvasRef.current.width;
      const amplitudesLength = Math.floor(
        width / (amplitudeSpacing + amplitudeWidth)
      );
      // taking the Math.ceil ensures there are more samples drawn than the canvas width
      const resampledLength = Math.ceil(
        (fftSize * amplitudesLength) / totalSamples
      );

      let amplitudes = Array(amplitudesLength).fill(-Infinity);
      let intervalId,
        numIntervals = Math.floor(totalSamples / fftSize);
      const timeDomainData = new Uint8Array(fftSize);
      const getAmplitudes = () => {
        analyser.getByteTimeDomainData(timeDomainData);
        // discard microphone silence
        if (timeDomainData.every((byte) => byte === 128)) return;

        amplitudes = amplitudes.slice(resampledLength);
        const resampled = resampleMaxAmplitudes(
          timeDomainData,
          resampledLength
        );
        amplitudes.push(...resampled);

        amplitudesRef.current = amplitudes;
        timeDataRef.current.push(...timeDomainData);

        if (--numIntervals === 0) {
          clearInterval(intervalId);
          onSecondsEnd(timeDataRef.current.slice());
        }
      };

      intervalId = setInterval(getAmplitudes, (fftSize / sampleRate) * 1e3);

      return function () {
        clearInterval(intervalId);
      };
    }
  }, [
    analyser,
    amplitudeSpacing,
    amplitudeWidth,
    canvasRef,
    numberOfSeconds,
    onSecondsEnd,
  ]);

  useEffect(() => {
    if (!analyser) {
      return;
    }
    let animationFrame;

    const draw = () => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      ctx.lineWidth = amplitudeWidth;
      ctx.strokeStyle = strokeStyle;

      const { height, width } = canvas;
      const midHeight = height / 2;

      let x = 5; // start at 5 to avoid drawing to border
      ctx.clearRect(0, 0, width, height);
      ctx.beginPath();
      for (const amplitude of amplitudesRef.current) {
        if (isFinite(amplitude)) {
          const y = Math.max(2, (amplitude / 255.0) * height);
          ctx.moveTo(x, midHeight - y / 2);
          ctx.lineTo(x, midHeight + y / 2);
        }
        x += amplitudeSpacing + amplitudeWidth;
      }
      ctx.stroke();
    };

    const render = () => {
      draw();
      animationFrame = requestAnimationFrame(render);
    };
    render();

    return function () {
      cancelAnimationFrame(animationFrame);
    };
  }, [amplitudeSpacing, amplitudeWidth, analyser, canvasRef, strokeStyle]);
};

export default useAnalyserRecorder;
