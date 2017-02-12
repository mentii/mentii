#!/bin/bash

pip install virtualenv
virtualenv -p python2.6 env
source env/bin/activate
pip install -r requirements.txt
