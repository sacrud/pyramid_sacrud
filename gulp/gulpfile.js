var gulp = require('gulp'),
    concat = require('gulp-concat');
    watch = require('gulp-watch');

var staticPath = '../pyramid_sacrud/static/';

gulp.task('concat', function() {
    gulp.src([
        staticPath + 'css/*.css',
        staticPath + 'css/**/*.css',
        '!' + staticPath + 'css/__main.css'
        ])
        .pipe(concat('__main.css'))
        .pipe(gulp.dest(staticPath + 'css/'));
});

gulp.task('watch', function () {
    watch([staticPath + 'css/*.css', staticPath + 'css/**/*.css',],
        function (files, cb) {
            gulp.start('concat', cb);
        });
});
