default: run

run:
	@ cd ./Backend; make -s
	@ cd ./Frontend; make -s

clean:
	@ cd ./Backend; make clean -s
	@ cd ./Frontend; make clean -s

compile:
	@ cd ./Frontend; make compile -s
