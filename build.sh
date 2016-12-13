#!/bin/bash

## $1 : branch_name

## Update git repo
echo "UPDATING GIT REPO"
cd /home/asp78/git/mentii
git fetch
git clean -fd
git checkout $1
git pull

## Move to buid_dir
echo "MOVING TO BUILD_DIR"
cp -R /home/asp78/git/mentii /home/asp78/build_dir/

## Remove .git and .gitignore
echo "REMOVING .git AND .gitignore FILES"
cd /home/asp78/build_dir
rm -rf ./mentii/.git ./mentii/.gitignore

## Build
echo "BUILDING PROJECT"
cd ./mentii
make compile
cd ..

## Tar it up and move it
echo "TARING UP AND MOVING PROJECT"
tar -cf build.tar ./mentii
mv --backup=numbered ./build.tar /home/asp78/public_html/builds/build.tar

echo "DONE!"
