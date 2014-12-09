var gulp = require('gulp'),
    gutil = require('gulp-util'),
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

gulp.task('watch', function () {

    var pathJS = glob.sync('./*/static/js/'),
        watchJSFiles = getFiles(pathJS, 'js');

    watch(watchJSFiles, function (files, cb) {
        gulp.start('browserify', cb);
    });
});

gulp.task('default', ['css', 'browserify']);