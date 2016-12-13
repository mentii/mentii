default:
	@ make -s run

run: clean
	@ pip install virtualenv
	@ virtualenv env
	@ xterm ./runBackend.sh &

run-lite:
	@ source env/bin/activate
	@ pip install -r requirements.txt
	@ python app.py

deploy: 
	@./updateBackendEnv.sh

clean:
	@ rm -rf ./env/
