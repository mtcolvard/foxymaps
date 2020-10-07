
const path = require('path')
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
// const LinkTypePlugin = require('html-webpack-link-type-plugin').HtmlWebpackLinkTypePlugin
const Dotenv = require('dotenv-webpack')
const minifyOptions = {
                collapseWhitespace: true,
                removeComments: true,
                removeRedundantAttributes: true,
                useShortDoctype: true,
                // removeStyleLinkTypeAttributes: false,
                // removeScriptTypeAttributes: false
            }



module.exports = {
  entry: './src/app.js',
  context: path.resolve(__dirname, 'frontend'),
  output: {
    // filename: 'bundle.js',
    filename: 'app.js',
    // path: path.resolve(__dirname, 'frontend/dist')
    path: path.resolve(__dirname, 'project/static'),
    publicPath: "/static/", // Should match Django STATIC_URL
    filename: "[name].js", // No filename hashing, Django takes care of this
    chunkFilename: "[id]-[chunkhash].js", // DO have Webpack hash chunk filename, see below
  },
  devtool: 'source-maps',
  module: {
    rules: [
      { test: /\.jsx?$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.css$/, loader: ['style-loader', 'css-loader'] },
      { test: /\.s(a|c)ss$/, loader: ['style-loader', 'css-loader', 'sass-loader'] },
      { test: /\.woff2?$/, loader: 'file-loader' },
      { test: /\.(jpg|png|gif)$/, loader: 'file-loader' }
    ]
  },
  devServer: {
    contentBase: path.join(__dirname, 'frontend/src'),
    hot: true,
    open: true,
    port: 8000,
    watchContentBase: true,
    proxy: {
      '/api': 'http://localhost:4000'
    },
  },
  plugins: [
    new Dotenv({
      path: path.resolve(__dirname, './.env'),
      systemvars: true
    }),
    new webpack.HotModuleReplacementPlugin(),
    // new HtmlWebpackPlugin({
    //   // template: 'src/index.html',
    //   filename: 'index.html',
    //   // inject: 'body',
    //   inject: false,
    //   template: require('html-webpack-template'),
    //   scripts: [
    //     'bundle.js',
    //     // {
    //     //   src: 'bundle.js',
    //     //   type: 'module'
    //     // }
    //   ],
    //   meta: {'Content-Type': {'http-equiv': 'Content-Type', 'content': 'text/javascript'}},
    //   minify: minifyOptions
    // }),
    // new LinkTypePlugin()
  ]
}
