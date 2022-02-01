/* Adapted from: https://github.com/onoya/react-mic-audio-visualizer */

import "webrtc-adapter"; // shims the getUserMedia to support a wider range of browsers
import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";

const UserMediaContext = createContext({
  stream: undefined,
  start: () => {},
  stop: () => {},
});

export const useMediaStream = () => useContext(UserMediaContext);

const UserMedia = ({ children, mediaStreamConstraints }) => {
  const [stream, setStream] = useState();

  const start = useCallback(async () => {
    setStream(
      await navigator.mediaDevices.getUserMedia(mediaStreamConstraints)
    );
  }, [mediaStreamConstraints]);

  const stopTracks = (stream) =>
    stream.getTracks().forEach((track) => track.stop());

  const stop = useCallback(() => {
    if (stream) {
      stopTracks(stream);
      setStream(undefined);
    }
  }, [stream]);

  useEffect(() => () => stream && stopTracks(stream), [stream]);

  return (
    <UserMediaContext.Provider
      value={{ stream, start, stop }}
      children={children}
    />
  );
};

export default UserMedia;
