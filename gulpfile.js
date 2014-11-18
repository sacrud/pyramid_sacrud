var autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    minifyCSS = require('gulp-minify-css'),
    watch = require('gulp-watch');

var _ = require("underscore"),
    browserify = require('browserify'),
    glob = require("glob"),
    minimatch = require("minimatch"),
    source = require('vinyl-source-stream');

function getFiles(path, type) {

    var files = glob.sync(path + '**/*.' + type);
    target = minimatch.match(files, '__*.' + type, { matchBase: true });
    ignore = _.map(target, function(item){ return '!' + item; });
    result = files.concat(ignore);

    if(type === undefined) { gutil.log(gutil.colors.red('Failed getFiles'), gutil.colors.yellow('type === undefined')); }
    if(files.length === 0) { gutil.log(gutil.colors.red('Failed getFiles'), gutil.colors.yellow('files not found, check path')); }

    return result;
}

gulp.task('browserify', function() {
    browserify('./pyramid_sacrud/static/js/main.js', { debug: false })
        .bundle()
        .on('error', function (err) {
            gutil.log(gutil.colors.red('Failed to browserify'), gutil.colors.yellow(err.message));
        })
        .pipe(source('__main.js'))
        .pipe(gulp.dest('./pyramid_sacrud/static/js/'));
});

gulp.task('css', function() {

    var path = glob.sync('./*/static/css/'),
        concatFiles = getFiles(path ,'css');

    gulp.src(concatFiles)
        .pipe(autoprefixer({
            browsers: [
                'Firefox >= 3',
                'Explorer >= 6',
                'Opera >= 9',
                'Chrome >= 15',
                'Safari >= 4',
                '> 1%'],
            cascade: false
        }))
        .on('error', function(err){
            gutil.log(gutil.colors.red('Failed to autoprefixer'), gutil.colors.yellow(err.message));
        })
        .pipe(minifyCSS())
        .pipe(concat('__sacrud.css'))
        .pipe(gulp.dest(path + '/'));
});


gulp.task('watch', function () {

    var pathCSS = glob.sync('./*/static/css/'),
        watchCSSFiles = getFiles(pathCSS, 'css');

    var pathJS = glob.sync('./*/static/js/'),
        watchJSFiles = getFiles(pathJS, 'js');

    watchJSFiles.push('!./pyramid_sacrud/static/js/bower_components/**/*');

    watch(watchCSSFiles, function (files, cb) {
        gulp.start('css', cb);
    });

    watch(watchJSFiles, function (files, cb) {
        gulp.start('browserify', cb);
    });
});

gulp.task('default', ['css', 'browserify']);