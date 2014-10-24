var gulp = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    minifyCSS = require('gulp-minify-css'),
    watch = require('gulp-watch'),
    browserify = require('browserify'),
    source = require('vinyl-source-stream');

var staticPath = '';
var cssFiles = ['../css/*.css', '../css/**/*.css', '!../css/__main.css'];
var jsFiles = ['../js/*.js', '../js/**/*.js', '!../js/__main.js'];

gulp.task('build', function () {
   gulp.src(cssFiles)
        .pipe(concat('style.min.css'))
        .pipe(minifyCSS())
        .pipe(gulp.dest(staticPath + 'build/'));
});

gulp.task('browserify', function() {
    browserify('./main.js', { debug: true })
        .bundle()
        .pipe(source('./__main.js'))
        .pipe(gulp.dest('./'));
});

gulp.task('css', function() {
    gulp.src(cssFiles)
        .pipe(autoprefixer({
            browsers: [
                'Firefox >= 3',
                'Explorer >= 6',
                'Opera >= 9',
                'Chrome >= 15',
                'Safari >= 4',
                '> 1%'
            ],
            cascade: false
        }))
        .pipe(concat('__main.css'))
        .pipe(gulp.dest(staticPath + 'css/'));
});

gulp.task('js', function() {
    gulp.src(jsFiles)
        .pipe(concat('__main.js'))
        .pipe(gulp.dest(staticPath + 'js/'));
});

gulp.task('watch', function () {
    watch(cssFiles, function (files) {
        return gulp.start('css');
    });
    watch(jsFiles, function (files) {
        return gulp.start('browserify');
    });
});
