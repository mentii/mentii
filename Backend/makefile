default:
	@ make -s run

run: clean
	@ cd ../../LocalDB; make -s
	@ pip install virtualenv
	@ virtualenv -p /usr/bin/python env
	@ osType=$(shell uname -a | awk -F " " '{print $$1}'); \
  if [ $$osType = Linux ]; then \
		xterm ./runBackend.sh &; \
	else \
		open -a Terminal ./runBackend.sh &; \
	fi

run-lite:
	@ cd ../../LocalDB; make -s
	@ osType=$(shell uname -a | awk -F " " '{print $$1}'); \
  if [ $$osType = Linux ]; then \
		xterm ./runBackend.sh &; \
	else \
		open -a Terminal ./runBackend.sh &; \
	fi

deploy:
	@ ./updateBackendEnv.sh

clean:
	@ rm -rf ./env/

runtests: clean
	@ cd ../../LocalDB; make -s
	@ ./runTests.sh
