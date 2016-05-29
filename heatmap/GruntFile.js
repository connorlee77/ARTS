module.exports = function(grunt) {
    grunt.initConfig({

        pkg: grunt.file.readJSON('package.json'),

        browserify: {
            dist: {
                options: {
                    transform: [
                        ['babelify', { presets: ['react'] }]
                    ]
                },
                src: 'public/js/*/*.js',
                dest: 'build/app.js'
            }
        },

        sass: { 
            dist: { 
                options: { 
                    style: 'expanded'
                },
                files: { 
                    'build/app.css': 'public/stylesheets/app.scss',
                }
            }
        },

        watch: {
            files: ["public/js/*/*.js", "public/stylesheets/*.scss"],
            tasks: ['browserify', 'sass']
        }
    })
    grunt.loadNpmTasks('grunt-browserify')
    grunt.loadNpmTasks('grunt-contrib-watch')
    grunt.loadNpmTasks('grunt-contrib-sass');
}
