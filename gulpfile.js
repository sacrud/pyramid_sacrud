var autoprefixer = require('gulp-autoprefixer'),
    batch = require('gulp-batch'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    minifyCSS = require('gulp-minify-css'),
    newer = require('gulp-newer'),
    sourcemaps = require('gulp-sourcemaps'),
    watch = require('gulp-watch');

var map = require('vinyl-map');

gulp.task('css', function() {
    patterns = ['./pyramid_sacrud/static/css/*.css', './pyramid_sacrud/static/css/**/*.css',
                '!./pyramid_sacrud/static/css/__sacrud.css'];
    gulp.src(patterns)
        .pipe(newer('./pyramid_sacrud/static/css/__sacrud.css'))
        .pipe(sourcemaps.init())
        .pipe(autoprefixer({
            browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9', 'Chrome >= 15', 'Safari >= 4', '> 1%'],
            cascade: false
        }))
        .on('error', function(err) {
            gutil.log(gutil.colors.red('Autoprefixer Error'), gutil.colors.yellow(err.message));
        })
        .pipe(minifyCSS())
        .pipe(concat('__sacrud.css'))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('./pyramid_sacrud/static/css/'))
        .pipe(map(function(code, filename) { gutil.log('CSS ' + gutil.colors.green(filename)); }))
        .on('error', gutil.log);

});


gulp.task('watch', function() {
    watch(['./pyramid_sacrud/static/css/*.css', './pyramid_sacrud/static/css/**/*.css',
           '!./pyramid_sacrud/static/css/__sacrud.css'], batch(function () {
        gulp.start('css');
        cb();
    }));
});

gulp.task('default', ['watch']);
