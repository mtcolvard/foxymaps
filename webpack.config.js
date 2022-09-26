const path = require('path')
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const Dotenv = require('dotenv-webpack')


module.exports = {
  // Tells the webpack that the front end is coming from the src folder in the front end
  mode: 'development',
  entry: './src/app.js',
  context: path.resolve(__dirname, 'frontend'),
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'frontend/dist')
  },
  devtool: 'source-map',
  // resolve: {
  //   extensions: ['.js', '.jsx', '.json', '.mjs', '.ts', '.tsx']
  // },
  // resolveLoader: {
  //   modules: ['node_modules'],
  //   extensions: ['.js', '.jsx', '.json', '.mjs', '.ts', '.tsx'],
  //   mainFields: ['babel-loader', 'main'],
  // },
  module: {
    rules: [
      { test: /\.m?js$/,
        resolve: {
          fullySpecified: false,
          extensions: ['.js', '.jsx', '.json', '.mjs', '.ts', '.tsx', '...']
        },
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
        }
      },
      { test: /\.css$/, use: [{loader: 'style-loader'}, {loader: 'css-loader'}] },
      { test: /\.s(a|c)ss$/, use: [{loader: 'style-loader'}, {loader: 'css-loader'}, {loader: 'sass-loader'}] },
      { test: /\.woff2?$/, type: 'asset/resource' },
      { test: /\.(jpg|png|gif)$/, type: 'asset/resource' }
    ]
  },
  devServer: {
    static: {
      directory: path.join(__dirname, 'frontend/src'),
    },
    hot: true,
    open: true,
    port: 8000,
    proxy: {
      '/api': 'http://localhost:4000'
    },
  },
  plugins: [
    new Dotenv({
      path: path.resolve(__dirname, './.env'),
      systemvars: true
      // ,
      // ignoreStub: true,
      // prefix: 'process.env.'
    }),
    new webpack.HotModuleReplacementPlugin(),
    new HtmlWebpackPlugin({
      template: 'src/index.html',
      filename: 'index.html',
      inject: 'body'
    })
  ]
}


// webpack 4 devserver config
// devServer: {
//   contentBase: path.join(__dirname, 'frontend/src'),
//   hot: true,
//   open: true,
//   port: 8000,
//   watchContentBase: true,
//   proxy: {
//     '/api': 'http://localhost:4000'
//   },
// webpack 4 modules config
// module: {
//   rules: [
//     { test: /\.(js)$/, exclude: /node_modules/, use: {loader: 'babel-loader'}, resolve: {fullySpecified: false}
//     },
//     { test: /\.css$/, use: [{loader: 'style-loader'}, {loader: 'css-loader'}] },
//     { test: /\.s(a|c)ss$/, use: [{loader: 'style-loader'}, {loader: 'css-loader'}, {loader: 'sass-loader'}] },
//     { test: /\.woff2?$/, loader: 'file-loader' },
//     { test: /\.(jpg|png|gif)$/, loader: 'file-loader' }
//   ]
// },



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
