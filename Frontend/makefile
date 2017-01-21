default: start

TERMINALSPAWNER=xterm -e
osType=$(shell uname -a | awk -F " " '{print $$1}')
ifeq ($(osType),Darwin)
	TERMINALSPAWNER=xterm -e
endif

clean:
	@ rm -rf ./node_modules
	@ cd app; find . -name "*.js.map" -type f -delete
	@ cd app; find . -name "*.js" -type f -delete

compile: clean
	@ npm install
	@ npm run-script tsc

compile-prod: clean
	@ npm install --production
	@ npm run-script tsc

runtests: compile
	@ npm run-script test

runtests-nocompile:
	@ npm run-script test

start: compile
	@ $(TERMINALSPAWNER) "./runFrontend.sh dev" &

run: compile-prod
	@ $(TERMINALSPAWNER) "./runFrontend.sh prod" &
