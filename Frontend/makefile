default: start

TERMINALSPAWNER=xterm -e
osType=$(shell uname -a | awk -F " " '{print $$1}')
ifeq ($(osType),Darwin)
	TERMINALSPAWNER=open -a Terminal
endif

clean:
	@ rm -rf ./node_modules
	@ cd app; find . -name "*.js.map" -type f -delete
	@ cd app; find . -name "*.js" -type f -delete

compile: clean
	@ npm install
	@ npm run-script tsc

runtests: compile
	@ ./node_modules/karma/bin/karma start

runtests-nocompile:
	@ ./node_modules/karma/bin/karma start

start: compile
	@ $(TERMINALSPAWNER) "./runFrontend.sh dev" &

run: compile
	@ $(TERMINALSPAWNER) "./runFrontend.sh prod" &
