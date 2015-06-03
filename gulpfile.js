'use strict';

var gulp = require('gulp'),
    plugins = require('gulp-load-plugins')({ pattern: ['gulp-*', 'gulp.*'] }),
    minifyCSS = require('gulp-minify-css');

var browserify = require('browserify'),
    browserSync = require('browser-sync'),
    buffer = require('vinyl-buffer'),
    map = require('vinyl-map'),
    mainBowerFiles = require('main-bower-files'),
    source = require('vinyl-source-stream');

var TARGET_CSS_FILE = '__pyramid_sacrud.css',
    TARGET_JS_FILE = '__pyramid_sacrud.js',
    TARGET_JS_LIB_FILE = '__pyramid_sacrud_libs.js';

var CSS_PATH = './pyramid_sacrud/static/css/',
    JS_PATH = './pyramid_sacrud/static/js/',
    IMG_PATH = './pyramid_sacrud/static/img/';

var TARGET_CSS_PATH = CSS_PATH + TARGET_CSS_FILE,
    TARGET_JS_PATH = JS_PATH + TARGET_JS_FILE;

var CSS_FILES = ['./pyramid_sacrud/static/css/*.css',
                 './pyramid_sacrud/static/css/**/*.css',
                 '!pyramid_sacrud/static/css/no-js.css',
                 '!pyramid_sacrud/static/css/' + TARGET_CSS_FILE
                ],
    JS_FILES = ['./pyramid_sacrud/static/js/*.js',
                './pyramid_sacrud/static/js/**/*.js',
                '!pyramid_sacrud/static/js/' + TARGET_JS_FILE,
                '!pyramid_sacrud/static/js/vendor/*.js'
               ],
    TEMPLATES_FILES = ['./pyramid_sacrud/**/*.jinja2','./example/**/*.jinja2'];

var BROWSERIFY_FILE = 'main.js',
    BROWSERIFY_LIBS = 'libs.js';


gulp.task('browser-sync', function() {
  browserSync({
    proxy: '127.0.0.1:6543',
    logLevel: 'silent'
  });
});


gulp.task('bower-js', function() {
  return gulp.src(mainBowerFiles({ filter: (/.*\.(js|map)$/i) }),
                 { base: 'bower_components' })
  .pipe(plugins.rename(function (path) {
    path.dirname = path.dirname.slice(0, path.dirname.indexOf('/') + 1);
  }))
  .pipe(gulp.dest(JS_PATH + 'vendor/'))
  .pipe(map(function(code, filename) {
    plugins.util.log('Bower JS ' +
    plugins.util.colors.green(filename));
  }));
});


gulp.task('bower-css', function() {
  return gulp.src(mainBowerFiles({ filter: (/.*\.(css)$/i) }),
                 { base: 'bower_components' })
  .pipe(plugins.rename(function (path) {
    path.dirname = path.dirname.slice(0, path.dirname.indexOf('/') + 1);
  }))
  .pipe(gulp.dest(CSS_PATH + 'vendor/'))
  .pipe(map(function(code, filename) {
    plugins.util.log('Bower CSS ' +
    plugins.util.colors.green(filename));
  }));
});


gulp.task('bower-img', function() {
  return gulp.src(mainBowerFiles({ filter: (/.*\.(png|jpg|gif)$/i) }),
                 { base: 'bower_components' })
  .pipe(plugins.rename(function (path) {
    path.dirname = path.dirname.slice(0, path.dirname.indexOf('/') + 1);
  }))
  .pipe(gulp.dest(IMG_PATH))
  .pipe(map(function(code, filename) {
    plugins.util.log('Bower Images ' +
    plugins.util.colors.green(filename));
  }));
});


gulp.task('browserify', function() {
  function bundle(b, sourceName) {
    b.bundle()
      .pipe(source(sourceName))
      .pipe(buffer())
      .pipe(plugins.sourcemaps.write('./'))
      .pipe(plugins.uglify())
      .pipe(gulp.dest('./pyramid_sacrud/static/js/'))
      .pipe(plugins.sourcemaps.init({loadMaps: true}))
      .pipe(
        map(function(code, filename) {
          plugins.util.log('Browserify ' + plugins.util.colors.green(filename));
        }))
      .pipe(browserSync.reload({ stream:true }));
  }
  bundle(browserify(
    { entries: './pyramid_sacrud/static/js/' + BROWSERIFY_LIBS }),
      TARGET_JS_LIB_FILE);
  bundle(browserify(
    { entries: './pyramid_sacrud/static/js/' + BROWSERIFY_FILE }),
      TARGET_JS_FILE);
});


gulp.task('css', function() {
  return gulp.src(CSS_FILES)
    .pipe(plugins.newer(TARGET_CSS_PATH))
    .pipe(plugins.sourcemaps.init())
    .pipe(plugins.autoprefixer({
      browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9',
                 'Chrome >= 15', 'Safari >= 4', '> 1%'],
      cascade: false
    }))
    .on('error', function(err) {
      plugins.util.log(plugins.util.colors.red('Autoprefixer Error'),
      plugins.util.colors.yellow(err.message));
    })
    .pipe(plugins.cssBase64({
      extensions: ['png', 'jpg', 'gif'],
      maxWeightResource: 100,
    }))
    .on('error', function(err) {
      plugins.util.log(plugins.util.colors.red('Base64 Error'),
      plugins.util.colors.yellow(err.message));
    })
    .pipe(plugins.concat(TARGET_CSS_FILE))
    .pipe(minifyCSS({ keepSpecialComments: 0 }))
    //.pipe(plugins.sourcemaps.write('.'))
    .pipe(gulp.dest(CSS_PATH))
    .on('error', plugins.util.log)
    .pipe(plugins.filter('*.css'))
    .pipe(map(function(code, filename) {
      plugins.util.log('CSS ' +
      plugins.util.colors.green(filename));
    }))
    .pipe(browserSync.reload({ stream:true }));
});


gulp.task('html', function() {
  return gulp.src(TEMPLATES_FILES)
    .pipe(browserSync.reload({ stream:true }));
});


gulp.task('watch', function() {
  plugins.watch(CSS_FILES,{ verbose: true },
    plugins.batch(function (cb) {
      gulp.start('css');
      cb();
    }));

  plugins.watch(JS_FILES, { verbose: true },
    plugins.batch(function (cb) {
      console.log(JS_FILES);
      gulp.start('browserify');
      cb();
    }));

  plugins.watch(TEMPLATES_FILES, { verbose: true },
    plugins.batch(function (cb) {
      gulp.start('html');
      cb();
    }));
});


gulp.task('default', ['browser-sync', 'watch']);
gulp.task('bower', ['bower-js', 'bower-css', 'bower-img']);
gulp.task('build', ['bower', 'css', 'browserify']);
