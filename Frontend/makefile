default: start

clean:
	@ rm -rf ./node_modules

compile: clean
	@ npm install

start: compile
	@ xterm -e "./runFrontend.sh dev" &

run: compile
	@ xterm -e "./runFrontend.sh prod" &
