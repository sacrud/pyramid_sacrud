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
    gulp.src(mainBowerFiles({filter: (/.*\.js$/i)}), { base: 'bower_components' })
        .pipe(gulp.dest('./pyramid_sacrud/static/js/__bower_components/'))
        .pipe(map(function(code, filename) { plugins.util.log('Bower JS ' + plugins.util.colors.green(filename));
    }))
    gulp.src(mainBowerFiles({filter: (/.*\.css$/i)}), { base: 'bower_components' })
        .pipe(gulp.dest('./pyramid_sacrud/static/css/__bower_components/'))
        .pipe(map(function(code, filename) { plugins.util.log('Bower CSS ' + plugins.util.colors.green(filename));
    }))
});

gulp.task('browserify', function() {

    var b = browserify({
        entries: './pyramid_sacrud/static/js/main.js',
        debug: true
    });

    b.bundle()
        .pipe(source('__pyramid_sacrud.js'))
        .pipe(buffer())
        .pipe(plugins.sourcemaps.init({loadMaps: true}))
        .pipe(plugins.sourcemaps.write('./'))
        .pipe(gulp.dest('./pyramid_sacrud/static/js/'))
        .pipe(map(function(code, filename) { plugins.util.log('Browserify ' + plugins.util.colors.green(filename)); }))
        .pipe(browserSync.reload({ stream:true }));
});

gulp.task('css', function() {
    path = ['./pyramid_sacrud/static/css/*.css',
            './pyramid_sacrud/static/css/**/*.css',
            '!./pyramid_sacrud/static/css/__pyramid_sacrud.css'];
    gulp.src(path)
        .pipe(plugins.newer('./pyramid_sacrud/static/css/__pyramid_sacrud.css'))
        .pipe(plugins.sourcemaps.init())
        .pipe(plugins.autoprefixer({
            browsers: ['Firefox >= 3', 'Explorer >= 6', 'Opera >= 9', 'Chrome >= 15', 'Safari >= 4', '> 1%'],
            cascade: false
        }))
        .on('error', function(err) {
            plugins.util.log(plugins.util.colors.red('Autoprefixer Error'), plugins.util.colors.yellow(err.message));
        })
        .pipe(minifyCSS())
        .pipe(plugins.concat('__pyramid_sacrud.css'))
        .pipe(plugins.sourcemaps.write('.'))
        .pipe(gulp.dest('./pyramid_sacrud/static/css/'))
        .pipe(map(function(code, filename) { plugins.util.log('CSS ' + plugins.util.colors.green(filename)); }))
        .on('error', plugins.util.log)
        .pipe(browserSync.reload({ stream:true }));
});

gulp.task('html', function() {
    gulp.src('./pyramid_sacrud/templates/**/*.jinja2')
        .pipe(browserSync.reload({ stream:true }));
});

gulp.task('watch', function() {
    plugins.watch(['./pyramid_sacrud/static/css/*.css',
                   './pyramid_sacrud/static/css/**/*.css',
                   '!./pyramid_sacrud/static/css/__pyramid_sacrud.css'],
                   { verbose: true }, plugins.batch(function (cb) {
        gulp.start('css');
        cb();
    }));
    plugins.watch(['./pyramid_sacrud/static/js/*.js',
                   './pyramid_sacrud/static/js/**/*.js',
                   '!pyramid_sacrud/static/js/__pyramid_sacrud.js'],
                   { verbose: true }, plugins.batch(function (cb) {
        gulp.start('browserify');
        cb();
    }));
    plugins.watch('./pyramid_sacrud/templates/**/*.jinja2',
                   { verbose: true }, plugins.batch(function (cb) {
        gulp.start('html');
        cb();
    }));
});


// gulp.task('build', function() {
//     gulp.src(['./pyramid_sacrud/static/css/__pyramid_sacrud.css', './pyramid_sacrud/static/js/__pyramid_sacrud.js'])
//         .pipe(plugins.rev())
//         .pipe(gulp.dest('./pyramid_sacrud/static/__build/'))
//         .pipe(map(function(code, filename) { plugins.util.log('Build Files ' + plugins.util.colors.green(filename)); }))
//         .pipe(plugins.rev.manifest('rev-manifest.json'))
//         .pipe(gulp.dest('./pyramid_sacrud/static/__build/'))
//         .pipe(map(function(code, filename) { plugins.util.log('Create Manifest ' + plugins.util.colors.green(filename)); }));

//     gulp.src('./pyramid_sacrud/templates/sacrud/base.jinja2')
//         .pipe(plugins.inject(
//             gulp.src(['./pyramid_sacrud/static/__build/*.js', './pyramid_sacrud/static/__build/*.css'], {read: false})))
//         .pipe(gulp.dest('./src'));
// });

gulp.task('default', ['watch', 'browser-sync']);