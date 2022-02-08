import { useCallback, useEffect, useRef, useState } from "react";

export const useMediaRecorder = (stream) => {
  const [blob, setBlob] = useState();
  const recorderRef = useRef();

  const stop = useCallback(
    () => recorderRef.current && recorderRef.current.stop()
  );

  useEffect(() => {
    if (stream) {
      const chunks = [];
      const recorder = new MediaRecorder(stream);

      recorder.onstop = (e) => {
        const blob = new Blob(chunks, { type: "audio/ogg; codecs=opus" });
        setBlob(blob);
      };

      recorder.ondataavailable = (e) => {
        chunks.push(e.data);
      };

      recorder.start();

      recorderRef.current = recorder;
    }
  }, [stream]);

  return { blob, stop };
};
