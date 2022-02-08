import { useEffect, useRef } from "react";

export const useByteTimeDomainDataRef = (analyser, bufferSeconds) => {
  const byteTimeDomainDataRef = useRef();

  useEffect(() => {
    if (analyser) {
      const fftSize = analyser.fftSize;
      const sampleRate = analyser.context.sampleRate;
      const timeDomainData = new Uint8Array(fftSize);
      byteTimeDomainDataRef.current = Array(sampleRate * bufferSeconds).fill(
        -Infinity
      );

      const intervalId = setInterval(() => {
        const queue = byteTimeDomainDataRef.current.slice(fftSize);
        analyser.getByteTimeDomainData(timeDomainData);
        queue.push(...timeDomainData);
        byteTimeDomainDataRef.current = queue;
      }, (fftSize / sampleRate) * 1e3);

      return function () {
        clearInterval(intervalId);
      };
    }
  }, [analyser, bufferSeconds]);

  return byteTimeDomainDataRef;
};
