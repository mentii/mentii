default:
#	@ make -s clean
	@ make -s compile
	@ make -s styles
	@ make -s run

styles:
	@ # Compile Bootstraps Less files into CSS and move to app/styles
	@ ./node_modules/less/bin/lessc ./node_modules/bootstrap/less/bootstrap.less ./app/styles/bootstrap.css
	@ # Minify CSS
	@ minify --no-comments ./app/styles/bootstrap.css
	@ # Remove unminified CSS file
	@ rm ./app/styles/bootstrap.css

compile:
	@ npm install

run:
	@ npm start

clean:
	@ rm -rf ./node_modules
