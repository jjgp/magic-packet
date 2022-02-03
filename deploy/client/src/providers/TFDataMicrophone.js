import React, { createContext, useContext, useEffect, useState } from "react";
import * as tf from "@tensorflow/tfjs";

const TFDataMicrophoneContext = createContext({
  mic: null,
  // TODO: add capture, isActive, start, stop to interface instead of exposing mic
});

export const useTFDataMicrophone = () => useContext(TFDataMicrophoneContext);

const TFDataMicrophone = ({ children, microphoneConfig }) => {
  const [mic, setMic] = useState();

  useEffect(() => {
    let createdMic;
    const createMic = async () => {
      createdMic = await tf.data.microphone(microphoneConfig);
      setMic(createdMic);
    };
    createMic();

    return function stop() {
      createdMic.stop();
    };
  }, [microphoneConfig]);

  return (
    <TFDataMicrophoneContext.Provider value={{ mic }} children={children} />
  );
};

export default TFDataMicrophone;
