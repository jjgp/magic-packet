/*global sampleRate*/

class DownsampleProcessor extends AudioWorkletProcessor {
  constructor(...args) {
    super(...args);
    // move following to initialize method
    this._frequencyBinCount = null;
    this._initialized = false;
    this._input = 0;
    this._channel = 0;
    this._sampleRate = null;
    this.port.onmessage = this._onmessage;
  }

  _linearInterpolate(input, outputLength) {
    // linear downsampling adapted from: https://stackoverflow.com/a/27437245
    const output = [];
    output[0] = input[0]; // keep start value
    // the distance between sampled values
    const skipDistance = (input.length - 1) / (outputLength - 1);
    for (let i = 1; i < outputLength - 1; ++i) {
      const pos = i * skipDistance;
      const i0 = Math.floor(pos);
      const i1 = Math.ceil(pos);
      // linearly interpolate input between indices i0 and i1
      output[i] = input[i0] + (pos - i0) * (input[i1] - input[i0]);
    }
    output[outputLength - 1] = input[input.length - 1]; // keep end value
    return output;
  }

  _onmessage = (event) => {
    console.log(event);
  };

  process(inputs, outputs, _) {
    if (this._initialized) {
      const input = inputs[this._input][this._channel];
      const outputLength = (this._sampleRate / sampleRate) * input.length;
      const downsampled = this._linearInterpolate(inputs, outputLength);
    }

    // just pass inputs through
    for (let n = 0; n < inputs.length; ++n) {
      // n inputs
      for (let m = 0; m < inputs[n].length; ++m) {
        // m channels
        outputs[n][m] = inputs[n][m];
      }
    }

    return true;
  }
}

registerProcessor("downsampleProcessor", DownsampleProcessor);
