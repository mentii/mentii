default:
	@ make -s run

run: clean
	@ pip install virtualenv
	@ virtualenv -p /usr/bin/python env
	@ xterm ./runBackend.sh &

run-lite:
	@ cd ../../LocalDB; make -s
	@ xterm ./runBackend.sh &

deploy:
	@ ./updateBackendEnv.sh

clean:
	@ rm -rf ./env/

runtests: clean
	@ cd ../../LocalDB; make -s
	@ ./runTests.sh
