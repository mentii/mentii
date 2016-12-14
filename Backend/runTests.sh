#!/bin/bash

pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python ./tests/test_user_ctrl.py
