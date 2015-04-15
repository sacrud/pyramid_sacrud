var gulp = require('gulp'),
    plugins = require('gulp-load-plugins')({ pattern: ['gulp-*', 'gulp.*'] }),
    minifyCSS = require('gulp-minify-css');

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
    return gulp.src(mainBowerFiles({filter: (/.*\.js$/i)}), { base: 'bower_components' })
        .pipe(gulp.dest('./static/js/__bower_components/'))
        .pipe(map(function(code, filename) { plugins.util.log('Bower JS ' + plugins.util.colors.green(filename));
    }))
    return gulp.src(mainBowerFiles({filter: (/.*\.css$/i)}), { base: 'bower_components' })
        .pipe(gulp.dest('./static/css/__bower_components/'))
        .pipe(map(function(code, filename) { plugins.util.log('Bower CSS ' + plugins.util.colors.green(filename));
    }))
});

gulp.task('browserify', function() {

    var b = browserify({ entries: './static/js/main.js' });

    //b.transform('browserify-shim', { global: true });

    return b.bundle()
        .pipe(source('__main.js'))
        .pipe(buffer())
        .pipe(plugins.sourcemaps.init({loadMaps: true}))
        .pipe(plugins.sourcemaps.write('./'))
        .pipe(gulp.dest('./static/js/'))
        .pipe(map(function(code, filename) { plugins.util.log('Browserify ' + plugins.util.colors.green(filename)); }))
        .pipe(browserSync.reload({ stream:true }));
});

gulp.task('css', function() {
    path = ['./static/css/*.css',
            './static/css/**/*.css',
            '!static/css/__main.css'];
    return gulp.src(path)
        .pipe(plugins.newer('./static/css/__main.css'))
        .pipe(plugins.sourcemaps.init())
        .pipe(plugins.autoprefixer({
            browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9', 'Chrome >= 15', 'Safari >= 4', '> 1%'],
            cascade: false
        }))
        .on('error', function(err) {
            plugins.util.log(plugins.util.colors.red('Autoprefixer Error'), plugins.util.colors.yellow(err.message));
        })
        .pipe(minifyCSS())
        .pipe(plugins.concat('__main.css'))
        .pipe(plugins.sourcemaps.write('.'))
        .pipe(gulp.dest('./static/css/'))
        .pipe(map(function(code, filename) { plugins.util.log('CSS ' + plugins.util.colors.green(filename)); }))
        .on('error', plugins.util.log)
        .pipe(browserSync.reload({ stream:true }));
});

gulp.task('html', function() {
    return gulp.src('./templates/**/*.html')
        .pipe(browserSync.reload({ stream:true }));
});


gulp.task('watch', function() {
    plugins.watch(['./static/css/*.css',
                   './static/css/**/*.css',
                   '!static/css/__main.css'],
                   { verbose: true }, plugins.batch(function (cb) {
        gulp.start('css');
        cb();
    }));
    plugins.watch(['./static/js/*.js',
                   './static/js/**/*.js',
                   '!static/js/__main.js'],
                   { verbose: true }, plugins.batch(function (cb) {
        gulp.start('browserify');
        cb();
    }));
    plugins.watch('./templates/**/*.html',
                   { verbose: true }, plugins.batch(function (cb) {
        gulp.start('html');
        cb();
    }));
});


gulp.task('default', ['watch', 'browser-sync']);