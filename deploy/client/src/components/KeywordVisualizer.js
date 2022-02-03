import { useEffect } from "react/cjs/react.development";
import { useTFDataMicrophone } from "../providers/TFDataMicrophone";

const KeywordVisualizer = ({ displayWidthInSeconds, ...props }) => {
  const { mic } = useTFDataMicrophone();

  useEffect(() => {
    if (!mic) {
      return;
    }

    let isDrawing = true;
    const draw = async () => {
      do {
        await new Promise(requestAnimationFrame);
      } while (isDrawing);
    };
    draw();

    return function stopDrawing() {
      isDrawing = false;
    };
  }, [mic]);

  return null;
};

export default KeywordVisualizer;
