default: start

clean:
	@ rm -rf ./node_modules
	@ cd app; find . -name "*.js.map" -type f -delete
	@ cd app; find . -name "*.js" -type f -delete

compile: clean
	@ npm install
	@ npm run-script tsc

runtests: compile
	@ ./node_modules/karma/bin/karma start

start: compile
	@ xterm -e "./runFrontend.sh dev" &

run: compile
	@ xterm -e "./runFrontend.sh prod" &
