var autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
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
    return result;
}

gulp.task('browserify', function() {
    browserify('./pyramid_sacrud/static/js/main.js', { debug: false })
        .bundle()
        .pipe(source('__main.js'))
        .pipe(gulp.dest('./pyramid_sacrud/static/js/'));
});

gulp.task('css', function() {

    var path = glob.sync('./*/static/css/'),
        concatFiles = getFiles(path);

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