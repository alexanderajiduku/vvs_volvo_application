const webpack = require('webpack');
const { addWebpackAlias } = require('customize-cra');

module.exports = function override(config) {
  config.resolve.fallback = {
    ...config.resolve.fallback,
    crypto: require.resolve('crypto-browserify'),
    stream: require.resolve('stream-browserify'),
  };

  
  return config;
};
