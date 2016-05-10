var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var STATIC_PATH = path.join(__dirname, './pyramid_sacrud/static/');
var JS_PATH = path.join('js');
var CSS_PATH = path.join('css');
var NODE_PATH = path.join(__dirname, 'node_modules')

config = {
  debug: true,
  devtool: 'source-map',
  context: STATIC_PATH,
  include: [path.resolve(JS_PATH)],
  entry: path.join(STATIC_PATH, JS_PATH, 'src', 'main.js'),
  output: {
    filename: path.join(JS_PATH, 'assets', '__[name].js'),
    path: STATIC_PATH,
    publicPath: "../"
  },
  resolveLoader: {
    root: NODE_PATH,
  },
  resolve: {
    unsafeCache: true,
    modulesDirectories: ['node_modules', 'bower_components'],
    alias: {
      'materialize-js': path.join(
        NODE_PATH, '/materialize-css/bin/materialize.js'
      ),
      'materialize-css': path.join(
        NODE_PATH, '/materialize-css/bin/materialize.css'
      ),
      jQuery: path.join(
        NODE_PATH, 'jquery/src/jquery.js'
      )
    }
  },
  module: {
    preLoaders: [{
      test: /jquery\/src\/selector-sizzle\.js$/,
      loader: 'string-replace',
      query: {
        search: '../external/sizzle/dist/sizzle',
        replace: 'sizzle'
      }
    }],
    loaders: [
      {
        test: /\.jsx?$/,
        loader: 'babel?presets=es2015',
        exclude: /(node_modules|bower_components)/
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract('style', 'css')
      },
      {
        test: /\.scss$/,
        loader: ExtractTextPlugin.extract(
          'style', 'css!postcss!sass'),
        exclude: /(node_modules|bower_components)/
      },
      {
        test: /\.(woff|woff2|eot|ttf)$/,
        loader: 'file',
        query: {
          name: path.join('fonts', '/[name].[ext]')
        }
      },
      {
        test: /\.(svg|png)$/,
        loader: 'file',
        query: {
          limit: 10000,
          name: path.join('img', '/[name].[ext]')
        }
      }
    ]
  },
  plugins: [
    new ExtractTextPlugin(path.join(CSS_PATH, '__main.css')),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.$": "jquery",
      "window.jQuery": "jquery"
    })
  ]
}

if (process.env.NODE_ENV == 'production') {
  plugins = [
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin()
  ]
  config['plugins'].concat(plugins);
  config['debug'] = false;
}
module.exports = config ;
