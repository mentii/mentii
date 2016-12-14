default:
	@ make -s run

run: clean
	@ pip install virtualenv
	@ virtualenv -p /usr/bin/python env
	@ xterm ./runBackend.sh &

run-lite:
	@ source env/bin/activate
	@ pip install -r requirements.txt
	@ python app.py

deploy: 
	@ ./updateBackendEnv.sh

clean:
	@ rm -rf ./env/

runtests:
	@ ./runTests.sh
