var gulp = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    clean = require('gulp-clean'),
    concat = require('gulp-concat'),
    minifyCSS = require('gulp-minify-css'),
    watch = require('gulp-watch'),
    browserify = require('browserify'),
    source = require('vinyl-source-stream');

var glob = require("glob");

var staticPath = '../';
var cssFiles = ['../css/*.css', '../css/**/*.css', '!../css/__main.css'];
var jsFiles = ['*.js', '**/*.js', '!gulpfile.js', '!__main.js'];

gulp.task('build', function () {
   gulp.src(cssFiles)
        .pipe(concat('style.min.css'))
        .pipe(minifyCSS())
        .pipe(gulp.dest(staticPath + 'build/'));
});

gulp.task('browserify', function() {
    browserify('./main.js', { debug: false })
        .bundle()
        .pipe(source('__main.js'))
        .pipe(gulp.dest('./'));
});

gulp.task('clean', function() {
    gulp.src(staticPath + 'css/__main.css', { read: false })
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
        .pipe(gulp.dest(staticPath + 'css/'));
});


gulp.task('watch', function () {
    watch(cssFiles, function (files) {
        return gulp.start('clean', 'css');
    });
});

gulp.task('default', ['clean', 'css', 'browserify']);

gulp.task('glob', function () {
    glob("app/**/*", {
        ignore: 'app/list.js'
    }, function (er, files) {
      console.log(files);
    });
});
