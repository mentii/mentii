#!/bin/bash

pip install virtualenv
virtualenv -p /usr/bin/python env
source env/bin/activate
pip install -r requirements.txt
