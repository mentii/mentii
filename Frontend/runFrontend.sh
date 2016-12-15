#!/bin/bash

if [ $1 == "prod" ]; then
	npm run package
	npm run live
elif [ $1 == "dev" ]; then
	npm start
else
	echo "Invalid argument given. Should be either 'prod' or 'dev'."
fi
