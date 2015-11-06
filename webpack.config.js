var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var STATIC_PATH = path.join(__dirname, './pyramid_sacrud/static/');
var JS_PATH = path.join(STATIC_PATH, 'js');
var CSS_PATH = path.join(STATIC_PATH, 'css');
var NODE_PATH = path.join(__dirname, 'node_modules')                                                  

config = {
  debug: true,
  context: STATIC_PATH,
  include: [path.resolve(JS_PATH)],
  entry: path.join(JS_PATH, 'src', 'main.js'),
  output: {filename: path.join(JS_PATH, 'assets', '__[name].js')},
  resolveLoader: {                                                                                
    root: NODE_PATH,                                                 
  },   
  resolve: {
    unsafeCache: true,
    modulesDirectories: ['node_modules', 'bower_components'],
    alias: {
      'materialize-js': path.join(
        NODE_PATH, '/materialize-css/dist/js/materialize.min.js'
      ),
      'materialize-css': path.join(
        NODE_PATH, '/materialize-css/dist/css/materialize.min.css'
      )
    }
  },
  module: {
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
          'style', 'css!resolve-url!autoprefixer!sass'),
        exclude: /(node_modules|bower_components)/
      },
      {
        test: /\.(woff|woff2|eot|ttf)$/,
        loader: 'file',
        query: {
          name: path.join(STATIC_PATH, 'fonts', '/[name].[ext]')
        }
      },
      {
        test: /\.(svg|png)$/,
        loader: 'file',
        query: {
          limit: 10000,
          name: path.join(STATIC_PATH, 'img') + '/[name].[ext]'
        }
      }
    ]
  },
  resolveUrlLoader: {
    absolute: '/prefix'
  },
  plugins: [
    new ExtractTextPlugin(path.join(CSS_PATH, '__main.css')),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
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
