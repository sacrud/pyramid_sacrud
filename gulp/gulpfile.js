var autoprefixer = require('gulp-autoprefixer'),
    browserify = require('browserify'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    source = require('vinyl-source-stream'),
    minifyCSS = require('gulp-minify-css'),
    watch = require('gulp-watch');

var staticPath = '../pyramid_sacrud/static/';
var cssFiles = [staticPath + 'css/*.css', staticPath + 'css/**/*.css', '!' + staticPath + 'css/__main.css'];
var jsFiles = [staticPath + 'js/*.js', staticPath + 'js/**/*.js', '!' + staticPath + 'js/__main.js'];

gulp.task('build', function () {
   gulp.src(cssFiles)
        .pipe(concat('style.min.css'))
        .pipe(minifyCSS())
        .pipe(gulp.dest(staticPath + 'build/'));
});

gulp.task('browserify', function() {
    browserify(staticPath + '/js/main.js', { debug: true })
        .bundle()
        .pipe(source('__main.js'))
        .pipe(gulp.dest(staticPath + './js/'));
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
                '> 1%'],
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