default: run

test:
	@ osType=$(shell uname -a | awk -F " " '{print $$1}'); \
  if [ $$osType = Linux ]; then \
		echo "IS LINUX"; \
	else \
		echo "IS NOT LINUX"; \
	fi

run:
	@ cd ../LocalDB; make -s
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
	@ cd ../LocalDB; make -s
	@ cd ./Frontend; make runtests -s
	@ cd ./Backend; make runtests -s

runtests-nocompile:
	@ cd ../LocalDB; make -s
	@ cd ./Frontend; make runtests-nocompile -s
	@ cd ./Backend; make runtests -s

setup:
	@ cd ../LocalDB; make -s run
	@ cd ./Backend; make -s
	@ cd ./Frontend; make -s
