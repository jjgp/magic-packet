/*global sampleRate*/

class DownSampleProcessor extends AudioWorkletProcessor {
  static get parameterDescriptors() {
    return [
      { name: "sampleRate", automationRate: "k-rate", defaultValue: 16000 },
    ];
  }

  process(inputs, outputs, parameters) {
    for (let n = 0; n < inputs.length; ++n) {
      // n inputs
      for (let m = 0; m < inputs[n].length; ++m) {
        // m channels
        const fitCount =
          (parameters.sampleRate[0] / sampleRate) * inputs[n][m].length;
        outputs[n][m] = this.downsample(inputs[n][m], fitCount);
      }
    }
    return true;
  }

  downsample(input, fitCount) {
    // Adapted from: https://stackoverflow.com/a/27437245
    const linearInterpolate = (before, after, atPoint) => {
      return before + (after - before) * atPoint;
    };

    const sampled = [];
    sampled[0] = input[0];
    const springFactor = Number((input.length - 1) / (fitCount - 1));
    for (let i = 1; i < fitCount - 1; ++i) {
      const tmp = i * springFactor;
      const before = Number(Math.floor(tmp)).toFixed();
      const after = Number(Math.ceil(tmp)).toFixed();
      const atPoint = tmp - before;
      sampled[i] = linearInterpolate(input[before], input[after], atPoint);
    }
    sampled[fitCount - 1] = input[input.length - 1]; // for new allocation
    return sampled;
  }
}

registerProcessor("downSampleProcessor", DownSampleProcessor);
