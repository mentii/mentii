default: run

run:
	@ cd ./Backend; make -s
	@ cd ./Frontend; make -s

clean:
	@ cd ./Backend; make clean -s
	@ cd ./Frontend; make clean -s

deploy:
	@ cd ./Backend; make deploy -s

compile:
	@ cd ./Frontend; make compile -s

runtests:
	@ cd ./Frontend; make runtests -s
	@ cd ./Backend; make runtests -s
