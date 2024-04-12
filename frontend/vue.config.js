const webpack = require('webpack')
const { VueLoaderPlugin } = require('vue-loader')
const { VuetifyPlugin } = require('webpack-plugin-vuetify')

module.exports = {
  publicPath: '',
  transpileDependencies: true,
  productionSourceMap: false,
  outputDir: 'dist',
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: 'true'
      }),
      new VuetifyPlugin(),
      new VueLoaderPlugin()
    ]
  }
}
