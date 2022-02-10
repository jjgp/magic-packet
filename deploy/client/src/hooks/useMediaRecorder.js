import { useEffect, useRef, useState } from "react";

export const useMediaRecorder = (stream) => {
  const [blob, setBlob] = useState();
  const recorderRef = useRef();

  const stop = () => recorderRef.current && recorderRef.current.stop();

  useEffect(() => {
    if (stream) {
      const recorder = new MediaRecorder(stream);

      recorder.ondataavailable = (e) => {
        const blob = new Blob([e.data], { type: "audio/ogg; codecs=opus" });
        setBlob(blob);
      };

      recorder.start();

      recorderRef.current = recorder;
    }
  }, [stream]);

  return { blob, stop };
};
