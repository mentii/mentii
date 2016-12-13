default:
	@ make -s run

run: clean
	@ pip install virtualenv
	@ virtualenv mentii_env
	@ xterm ./runBackend.sh &

run-lite:
	@ source mentii_env/bin/activate
	@ pip install -r requirements.txt
	@ python app.py

clean:
	@ rm -rf ./mentii_env/
