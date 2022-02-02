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

  const stop = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
  }, [stream]);

  useEffect(() => () => stop(), [mediaStreamConstraints, stop]);

  return (
    <UserMediaContext.Provider
      value={{ stream, start, stop }}
      children={children}
    />
  );
};

export default UserMedia;
