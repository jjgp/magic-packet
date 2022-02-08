/*
  Adapted from:
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/AudioAnalyserContext.tsx
    - https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/AudioVisualizer.tsx
*/

import { useEffect, useRef } from "react";
import { useSourceAnalyser } from ".";

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

export const useAudioVisualizer = (
  source,
  canvasRef,
  amplitudeSpacing = 3,
  amplitudeWidth = 2,
  displaySeconds = 3,
  strokeStyle = "#fff"
) => {
  const analyser = useSourceAnalyser(source);
  const amplitudesRef = useRef([]);

  useEffect(() => {
    if (analyser) {
      const fftSize = analyser.fftSize;
      const sampleRate = analyser.context.sampleRate;
      const width = canvasRef.current.width;
      const amplitudesLength = Math.floor(
        width / (amplitudeSpacing + amplitudeWidth)
      );
      const resampledLength = Math.floor(
        (fftSize * amplitudesLength) / (sampleRate * displaySeconds)
      );

      let amplitudes = Array(amplitudesLength).fill(-Infinity);
      const timeDomainData = new Uint8Array(fftSize);
      const intervalId = setInterval(() => {
        amplitudes = amplitudes.slice(resampledLength);
        analyser.getByteTimeDomainData(timeDomainData);
        const resampled = resampleMaxAmplitudes(
          timeDomainData,
          resampledLength
        );
        amplitudes.push(...resampled);
        amplitudesRef.current = amplitudes;
      }, (fftSize / sampleRate) * 1e3);

      return function () {
        clearInterval(intervalId);
      };
    }
  }, [analyser, amplitudeSpacing, amplitudeWidth, canvasRef, displaySeconds]);

  useEffect(() => {
    let animationFrame;

    const draw = () => {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      ctx.lineWidth = amplitudeWidth;
      ctx.strokeStyle = strokeStyle;

      const { height, width } = canvas;
      const midHeight = height / 2;

      let x = 0;
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

    return () => {
      cancelAnimationFrame(animationFrame);
    };
  }, [amplitudeSpacing, amplitudeWidth, canvasRef, strokeStyle]);
};

export default useAudioVisualizer;
