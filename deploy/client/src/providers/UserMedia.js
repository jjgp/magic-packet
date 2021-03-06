/* Adapted from: https://github.com/onoya/react-mic-audio-visualizer/blob/master/src/contexts/MediaStreamContext.tsx */

import "webrtc-adapter"; // shims the getUserMedia to support a wider range of browsers
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";

const UserMediaContext = createContext({
  stream: null,
  start: () => {},
  stop: () => {},
});

export const useUserMedia = () => useContext(UserMediaContext);

const UserMedia = ({ children, mediaStreamConstraints }) => {
  const [stream, setStream] = useState();

  const start = useCallback(async () => {
    setStream(
      await navigator.mediaDevices.getUserMedia(mediaStreamConstraints)
    );
  }, [mediaStreamConstraints]);

  const stopStream = (stream) => {
    if (stream && stream.active) {
      stream.getTracks().forEach((track) => track.stop());
    }
  };

  const stop = useCallback(() => {
    stopStream(stream);
    setStream(null);
  }, [stream]);

  useEffect(() => {
    const previousStream = stream;
    return function () {
      stopStream(previousStream);
    };
  }, [stream]);

  return (
    <UserMediaContext.Provider
      value={{ stream, start, stop }}
      children={children}
    />
  );
};

export default UserMedia;
