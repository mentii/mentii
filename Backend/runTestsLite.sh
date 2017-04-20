#!/bin/bash

source env/bin/activate
nose2 -c config/unittest.cfg
