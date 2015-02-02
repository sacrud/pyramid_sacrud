var gulp = require('gulp'),
    autoprefixer = require('gulp-autoprefixer'),
    clean = require('gulp-clean'),
    concat = require('gulp-concat'),
    filter = require('gulp-filter'),
    minifyCSS = require('gulp-minify-css'),
    gutil = require('gulp-util'),
    watch = require('gulp-watch');

var _ = require("underscore"),
    browserify = require('browserify'),
    glob = require("glob"),
    mainBowerFiles = require('main-bower-files'),
    minimatch = require("minimatch"),
    path = require('path'),
    map = require('vinyl-map'),
    source = require('vinyl-source-stream');

function getFiles(path, type) {

    var files = glob.sync(path + '**/*.' + type);
    target = minimatch.match(files, '__*.' + type, { matchBase: true });
    ignore = _.map(target, function(item){ return '!' + item; });
    result = files.concat(ignore);

    if(type === undefined) { gutil.log(gutil.colors.red('Failed getFiles'), gutil.colors.yellow('type === undefined')); }
    if(files.length === 0) { gutil.log(gutil.colors.red('Failed getFiles'), gutil.colors.yellow('files not found, check path')); }

    return result;
}

// get css and js files from bower components
var css_path = glob.sync('./*/static/css/');
var js_path = glob.sync('./*/static/js/');
var components = glob.sync('./bower_components/*').map(function(componentDir) {
        return path.basename(componentDir);
    });

components.forEach(function(name) {

    gulp.task(name+'-clean', function(done) {
        // gulp.src(js_path + '/lib/' + name + '/').pipe(clean());
        gulp.src(css_path + '/lib/' + name + '/').pipe(clean()).on('end', done);
    });

    // copy css files from bower component to static dir in project
    gulp.task(name+'-css', function(done) {
        gulp.src(mainBowerFiles('**/' + name + '/**'))
            .pipe(filter('*.css'))
            .pipe(gulp.dest(css_path + '/lib/' + name + '/'))
            .pipe(map(function(code, filename) { gutil.log('Copy ' + gutil.colors.green(filename)); }))
            .on('end', done);
    });

    // copy js files from bower component to static dir in project
    gulp.task(name+'-js', function(done) {
        gulp.src(mainBowerFiles('**/' + name + '/**'))
            .pipe(filter('*.js'))
            .pipe(gulp.dest(js_path + '/lib/' + name + '/'))
            .pipe(map(function(code, filename) { gutil.log('Copy ' + gutil.colors.green(filename)); }))
            .on('end', done);
    });

    // build component by name
    gulp.task(name+'-build', [name+'-clean', name+'-css', name+'-js']);
});

// build all components
gulp.task('build-components', components.map(function(name){ return name+'-build'; }));


gulp.task('css', ['pickadate-clean', 'pickadate-css'], function() {
    var path = glob.sync('./*/static/css/'),
        concatFiles = getFiles(path ,'css');

    gulp.src(concatFiles)
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
        .on('error', function(err){
            gutil.log(gutil.colors.red('Failed to autoprefixer'), gutil.colors.yellow(err.message));
        })
        .pipe(minifyCSS())
        .pipe(concat('__sacrud.css'))
        .pipe(gulp.dest(path + '/'));
});

gulp.task('browserify', function() {
    browserify('./pyramid_sacrud/static/js/main.js', { debug: false })
        .bundle()
        .on('error', function (err) {
            gutil.log(gutil.colors.red('Failed to browserify'), gutil.colors.yellow(err.message));
        })
        .pipe(source('__main.js'))
        .pipe(gulp.dest('./pyramid_sacrud/static/js/'));
});

gulp.task('watch', function () {

    // var pathCSS = glob.sync('./*/static/css/'),
    //     watchCSSFiles = getFiles(pathCSS, 'css');

    var pathJS = glob.sync('./*/static/js/'),
        watchJSFiles = getFiles(pathJS, 'js');

    // watch(watchCSSFiles, function (files, cb) {
    //     gulp.start('css', cb);
    // });

    watch(watchJSFiles, function (files, cb) {
        gulp.start('browserify', cb);
    });
});

gulp.task('default', ['browserify']);
