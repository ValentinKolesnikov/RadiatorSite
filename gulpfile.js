var gulp      = require('gulp'), // Подключаем Gulp
	sass        = require('gulp-sass');

gulp.task('sass-django', function(){
	return gulp.src('mainApp/static/sass/**/*.sass') // Берем все sass файлы из папки sass и дочерних, если таковые будут
		.pipe(sass())
		.pipe(gulp.dest('mainApp/static/css'))
});

gulp.task('sass', function(){
	return gulp.src('currentVersion/sass/**/*.sass') // Берем все sass файлы из папки sass и дочерних, если таковые будут
		.pipe(sass())
		.pipe(gulp.dest('currentVersion/css'))
});

gulp.task('watch-django', function() {
	gulp.watch('mainApp/static/sass/**/*.sass', gulp.parallel('sass-django'))
});

gulp.task('watch-front', function() {
	gulp.watch('currentVersion/sass/**/*.sass', gulp.parallel('sass'))
});