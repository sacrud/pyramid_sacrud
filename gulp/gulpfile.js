var browserify = require('browserify'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    //merge = require('merge-stream'),
    source = require('vinyl-source-stream'),
    watch = require('gulp-watch');

var staticPath = '../pyramid_sacrud/static/';
var cssFiles = [staticPath + 'css/*.css', staticPath + 'css/**/*.css', '!' + staticPath + 'css/__main.css'];
var jsFiles = [staticPath + 'js/*.js', staticPath + 'js/**/*.js', '!' + staticPath + 'js/__main.js'];


gulp.task('default', function () {
   // Your default task
});

gulp.task('browserify', function() {
    return browserify(staticPath + '/js/main.js')
    .bundle()
    .pipe(source('__main.js'))
    .pipe(gulp.dest(staticPath + './js/'));
});

gulp.task('css', function() {
    gulp.src(cssFiles)
        .pipe(concat('__main.css'))
        .pipe(gulp.dest(staticPath + 'css/'));
});

gulp.task('js', function() {
    gulp.src(jsFiles)
        .pipe(concat('__main.js'))
        .pipe(gulp.dest(staticPath + 'js/'));
});

gulp.task('watch', function () {
    gulp.src(cssFiles)
        .pipe(watch(cssFiles, function (files) {
            gulp.start('css');
        }));
    gulp.src(jsFiles)
        .pipe(watch(jsFiles, function (files) {
            gulp.start('browserify');
        }));
});