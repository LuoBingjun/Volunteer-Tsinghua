var gulp = require('gulp');
var less = require('gulp-less');
var rename = require('gulp-rename');
var postcss = require('gulp-postcss');
var cssnano = require('gulp-cssnano');
var header = require('gulp-header');
var autoprefixer = require('autoprefixer');
var pkg = require('./package.json');

gulp.task('watch', function() {
  gulp.watch('./**', []);
});

gulp.task('default', function(){
    gulp
    .src(
      [
        './app.js',
        './app.json',
        './app.wxss',
        '**'
      ],
      { base: '.' }
    )
});