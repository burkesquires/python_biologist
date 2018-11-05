const gulp = require('gulp');
const sync = require('browser-sync').create();

// Server

gulp.task('default', [], () => {
	sync.init({
		ui: false,
		notify: false,
		server: {
			baseDir: './slides',
			index: 'index.html'
		}
	});

	gulp.watch('./slides/index.html').on('change', sync.reload);
});

