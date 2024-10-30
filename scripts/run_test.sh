#!/bin/bash

# Activate the virtual environment
source venv/bin/activate


echo " - Starting all tests  \n"

echo " -------- Testing Calculator --------"
pytest tests/test_calculator.py

echo "\n -------- Testing PStar Strategy --------"
pytest tests/test_pstar_strategy.py

echo "\n -------- Testing Equi No Packing Strategy --------"
pytest tests/test_equi_nr_strategy.py

echo "\n -------- Testing Prob7.py  --------"
pytest tests/test_prob7.py

echo "\n -------- Testing util.py  --------"
# pytest tests/test_util.py -v -s
pytest tests/test_util.py 