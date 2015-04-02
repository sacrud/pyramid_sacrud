var autoprefixer = require('gulp-autoprefixer'),
    batch = require('gulp-batch'),
    concat = require('gulp-concat'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    minifyCSS = require('gulp-minify-css'),
    newer = require('gulp-newer'),
    sourcemaps = require('gulp-sourcemaps'),
    watch = require('gulp-watch');

var browserify = require('browserify'),
    browserSync = require('browser-sync'),
    buffer = require('vinyl-buffer'),
    map = require('vinyl-map'),
    mainBowerFiles = require('main-bower-files'),
    source = require('vinyl-source-stream');

gulp.task('browser-sync', function() {
    browserSync({
        proxy: "127.0.0.1:6543",
        logLevel: "silent",
    });
});

gulp.task('bower', function() {
    // gulp.src(mainBowerFiles({filter: (/.*\.js$/i)}), { base: 'bower_components' })
    //     .pipe(gulp.dest('./pyramid_sacrud/static/js/__bower_components/'))
    //     .pipe(map(function(code, filename) { gutil.log('Bower JS ' + gutil.colors.green(filename));
    // }))
    gulp.src(mainBowerFiles({filter: (/.*\.css$/i)}), { base: 'bower_components' })
        .pipe(gulp.dest('./pyramid_sacrud/static/css/__bower_components/'))
        .pipe(map(function(code, filename) { gutil.log('Bower CSS ' + gutil.colors.green(filename));
    }))
});

gulp.task('browserify', function() {
    browserify('./pyramid_sacrud/static/js/main.js')
        .bundle()
        .pipe(source('__pyramid_sacrud.js'))
        .pipe(buffer())
        .pipe(sourcemaps.init({loadMaps: true}))
        .pipe(sourcemaps.write('./'))
        .pipe(gulp.dest('./pyramid_sacrud/static/js/'))
        .pipe(map(function(code, filename) { gutil.log('Browserify ' + gutil.colors.green(filename)); }))
        .pipe(browserSync.reload({ stream:true }));
});

gulp.task('css', function() {
    path = ['./pyramid_sacrud/static/css/*.css',
            './pyramid_sacrud/static/css/**/*.css',
            '!./pyramid_sacrud/static/css/__pyramid_sacrud.css'];
    gulp.src(path)
        .pipe(newer('./pyramid_sacrud/static/css/__pyramid_sacrud.css'))
        .pipe(sourcemaps.init())
        .pipe(autoprefixer({
            browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9', 'Chrome >= 15', 'Safari >= 4', '> 1%'],
            cascade: false
        }))
        .on('error', function(err) {
            gutil.log(gutil.colors.red('Autoprefixer Error'), gutil.colors.yellow(err.message));
        })
        .pipe(minifyCSS())
        .pipe(concat('__pyramid_sacrud.css'))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('./pyramid_sacrud/static/css/'))
        .pipe(map(function(code, filename) { gutil.log('CSS ' + gutil.colors.green(filename)); }))
        .on('error', gutil.log)
        .pipe(browserSync.reload({ stream:true }));
});

gulp.task('watch', function() {
    watch(['./pyramid_sacrud/static/css/*.css',
           './pyramid_sacrud/static/css/**/*.css',
           '!./pyramid_sacrud/static/css/__pyramid_sacrud.css'], batch(function () {
        gulp.start('css');
        cb();
    }));
});

gulp.task('default', ['watch', 'browser-sync']);