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

runtests-nocompile:
	@ ./node_modules/karma/bin/karma start

start: compile
	@ osType=$(shell uname -a | awk -F " " '{print $$1}'); \
  if [ $$osType = Linux ]; then \
		xterm -e "./runFrontend.sh dev" &; \
	else \
		open -a Terminal "./runFrontend.sh dev" &; \
	fi

run: compile
	@ osType=$(shell uname -a | awk -F " " '{print $$1}'); \
  if [ $$osType = Linux ]; then \
		xterm -e "./runFrontend.sh prod" &; \
	else \
		open -a Terminal "./runFrontend.sh prod" &; \
	fi
