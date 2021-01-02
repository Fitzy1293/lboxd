#!/bin/env bash

clear
python3 'tests.py'
python3 'cli_test.py' -trw && cat 'testfitzy1293_all_reviews.html'
