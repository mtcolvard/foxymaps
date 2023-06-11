const path = require('path')
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const Dotenv = require('dotenv-webpack')

module.exports = {
  // Don't forget to set this to production
  mode: 'development',
  // Tells the webpack that the front end is coming from the src folder in the front end
  entry: './src/app.js',
  context: path.resolve(__dirname, 'frontend'),
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'frontend/dist')
  },
  devtool: 'source-map',
  module: {
    rules: [
    //loader: in webpack4 has been changed to use: in webpack5
      {
        test: /\.m?js$/, use: 'babel-loader', exclude: /node_modules/, resolve: {
          fullySpecified: false, extensions: ['.mjs', '.js', '...']
        } },
      { test: /\.css$/, use: ['style-loader', 'css-loader'] },
      { test: /\.s(a|c)ss$/, use: ['style-loader', 'css-loader', 'sass-loader'], resolve: {
        fullySpecified: false,
      } },
      { test: /\.woff2?$/, use: 'file-loader' },
      { test: /\.(jpg|png|gif)$/, use: 'file-loader' }
    ]
  },
  
  devServer: {
    static: path.join(__dirname, 'frontend/src'),
    hot: true,
    open: true,
    port: 8000,
    // watchContentBase: true,
    // watch: true,
    proxy: {
      '/api': 'http://localhost:4000'
    },
  },
  plugins: [
    new Dotenv({
      path: path.resolve(__dirname, './.env'),
      systemvars: true
    }),
    // new webpack.HotModuleReplacementPlugin(),
    new HtmlWebpackPlugin({
      template: 'src/index.html',
      filename: 'index.html',
      inject: 'body'
    })
  ]
}

//
// const LinkTypePlugin = require('html-webpack-link-type-plugin').HtmlWebpackLinkTypePlugin
// const minifyOptions = {
//                 collapseWhitespace: true,
//                 removeComments: true,
//                 removeRedundantAttributes: true,
//                 useShortDoctype: true,
//                 // removeStyleLinkTypeAttributes: false,
//                 // removeScriptTypeAttributes: false
//             }
// module.exports = {
//   entry: './src/app.js',
//   context: path.resolve(__dirname, 'frontend'),
//   output: {
//     filename: 'bundle.js',
//     path: path.resolve(__dirname, 'frontend/dist')
//   },
//   devtool: 'source-maps',
//   plugins: [
//     new Dotenv({
//       path: path.resolve(__dirname, './.env'),
//       systemvars: true
//     }),
//     new webpack.HotModuleReplacementPlugin(),
//     new HtmlWebpackPlugin({
//       // template: 'src/index.html',
//       filename: 'index.html',
//       // inject: 'body',
//       inject: false,
//       template: require('html-webpack-template'),
//       scripts: [
//         'bundle.js',
//         // {
//         //   src: 'bundle.js',
//         //   type: 'module'
//         // }
//       ],
//       meta: {'Content-Type': {'http-equiv': 'Content-Type', 'content': 'text/javascript'}},
//       minify: minifyOptions
//     }),
//     // new LinkTypePlugin()
//   ]
// }
