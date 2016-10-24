## Default make command ##
default:
	@ make --no-print-directory clean
	@ make --no-print-directory install
	@ make --no-print-directory start

## Removes directorys containing package dependencies ##
clean:
	@ rm -rf ./dist/ ./node_modules/ ./src/node_modules/ ./src/typings/

## Installs fresh version of the application ##
install:
	@ make --no-print-directory clean
	@ npm install
	@ cd ./src; npm install

## Runs local dev instance, for quick testing  ##
start:
	@ cd ./src; npm start

## Runs in deployable state, use before commiting ##
run:
	@ npm run package
	@ npm run live
