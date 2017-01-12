default: run

run:
	@ cd ./Backend; make -s
	@ cd ./Frontend; make -s

clean:
	@ cd ./Backend; make clean -s
	@ cd ./Frontend; make clean -s

clean-hard: clean
	@ cd ../LocalDB; make clean -s
	@ rm -rf ./logs/

deploy:
	@ cd ./Backend; make deploy -s

compile:
	@ cd ./Frontend; make compile -s

runtests:
	@ cd ./Frontend; make runtests -s
	@ cd ./Backend; make runtests -s

runtests-nocompile:
	@ cd ./Frontend; make runtests-nocompile -s
	@ cd ./Backend; make runtests -s