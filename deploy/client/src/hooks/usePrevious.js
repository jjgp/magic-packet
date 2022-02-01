/* Adapted from: https://blog.logrocket.com/accessing-previous-props-state-react-hooks/ */

import { useEffect, useRef } from "react";

const usePrevious = (value) => {
  const ref = useRef();
  useEffect(() => {
    ref.current = value;
  }, [value]);
  return ref.current;
};

export default usePrevious;
