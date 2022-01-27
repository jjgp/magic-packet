const tf = require("@tensorflow/tfjs");

function resnet8(
  inputs,
  n_outputs,
  n_blocks = 3,
  filters = 45,
  pooling = [4, 3]
) {
  const convargs = {
    filters: filters,
    kernelSize: 3,
    activation: "relu",
    useBias: false,
    padding: "same",
  };

  let x = tf.layers.conv2d(convargs).apply(inputs);
  x = tf.layers.avgPool2d({ poolSize: pooling, padding: "same" }).apply(x);

  let skip = x;
  for (let i = 1; i < 2 * n_blocks + 1; ++i) {
    x = tf.layers.conv2d(convargs).apply(x);
    if (i > 0 && i % 2 === 0) x = skip = tf.layers.add().apply([x, skip]);
    x = tf.layers.batchNormalization({ center: false, scale: false }).apply(x);
  }
  x = tf.layers.avgPool2d({ pool_size: x.shape.slice(1, 3) }).apply(x);
  x = tf.layers.dense({ units: n_outputs }).apply(x);
  outputs = tf.layers.reshape({ targetShape: [n_outputs] }).apply(x);
  return tf.model({ inputs, outputs, name: "resnet8" });
}

const inputs = tf.input({ shape: [124, 13, 1] });
const model = resnet8(inputs, 8);
model.summary();

await model.loadWeights("./resnet8_weights.h5", false);
