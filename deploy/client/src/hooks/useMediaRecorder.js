import { useEffect, useRef, useState } from "react";

export const useMediaRecorder = (stream, timeslice) => {
  const [blob, setBlob] = useState();
  const recorderRef = useRef();

  const stop = () => recorderRef.current && recorderRef.current.stop();

  useEffect(() => {
    if (stream) {
      const recorder = new MediaRecorder(stream, {
        audioBitsPerSecond: 24 * stream.context.sampleRate,
      });

      recorder.ondataavailable = (e) => {
        const blob = new Blob([e.data], { type: "audio/ogg; codecs=opus" });
        setBlob(blob);
      };

      recorder.start(timeslice);

      recorderRef.current = recorder;
    }
  }, [stream, timeslice]);

  return { blob, stop };
};
