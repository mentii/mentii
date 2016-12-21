default:
	@ make -s run

TERMINALSPAWNER=xterm -e
osType=$(shell uname -a | awk -F " " '{print $$1}')
ifeq ($(osType),Darwin)
	TERMINALSPAWNER=xterm -e
endif

run: clean
	@ cd ../../LocalDB; make -s
	@ pip install virtualenv
	@ virtualenv -p /usr/bin/python env
	@ $(TERMINALSPAWNER) ./runBackend.sh &

run-lite:
	@ cd ../../LocalDB; make -s
	@ $(TERMINALSPAWNER) ./runBackend.sh &

deploy:
	@ ./updateBackendEnv.sh

clean:
	@ rm -rf ./env/
	@ find . -name "*.pyc" -type f -delete

runtests: clean
	@ cd ../../LocalDB; make -s
	@ ./runTests.sh
