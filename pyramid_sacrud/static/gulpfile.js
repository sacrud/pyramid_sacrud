var gulp = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    clean = require('gulp-clean'),
    concat = require('gulp-concat'),
    minifyCSS = require('gulp-minify-css'),
    watch = require('gulp-watch'),
    browserify = require('browserify'),
    source = require('vinyl-source-stream');

var glob = require("glob");

var cssFiles = ['css/*.css', 'css/**/*.css', '!css/__main.css'];
var jsFiles = ['js/*.js', 'js/**/*.js', '!js/__main.js'];

gulp.task('build', function () {
   gulp.src(cssFiles)
        .pipe(concat('style.min.css'))
        .pipe(minifyCSS())
        .pipe(gulp.dest('build/'));
});

gulp.task('browserify', function() {
    browserify('./js/main.js', { debug: false })
        .bundle()
        .pipe(source('__main.js'))
        .pipe(gulp.dest('js/'));
});

gulp.task('clean', function() {
    gulp.src('css/__main.css', { read: false })
        .pipe(clean({ force: true }));
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
        .pipe(gulp.dest('css/'));
});


gulp.task('watch', function () {
    watch(cssFiles, function (files) {
        return gulp.start('clean', 'css');
    });
    watch(jsFiles, function (files) {
        return gulp.start('browserify');
    });
});

gulp.task('default', ['clean', 'css', 'browserify']);

gulp.task('glob', function () {
    glob("js/app/**/*", {
        ignore: 'js/app/list.js'
    }, function (er, files) {
      console.log(files);
    });
});
