### linting

pylint combined_hetro_plot.py

### To execute tree command with own code excluding folders

tree -P "_.py|_.png|_.txt|_.env|\*.json" -I "venv|**pycache**|.git|.pytest_cache|spikes" --prune

## appending -d only shows directory

tree -P "_.py|_.png|_.txt|_.env|\*.json" -I "venv|**pycache**|.git|.pytest_cache|spikes" --prune -d

### Running the tests

pytest tests/test_util.py -v -s

| -v flag show me the results
| -s flag show the prints

### To run usage files, use this command to add the project root directly to the PYTHONPATH

#### Execute this from the terminal in project root folder.

#### as unlike pytest by default python does include the root directory path

export PYTHONPATH="$(pwd):$PYTHONPATH"

### printing detailed trace

#### and directing the output to the trace_dump folder

python -m trace --trace main.py > trace_dump/trace2

### using built in profiler 'cprofile' to get function call statistics

python -m cProfile -o trace_o.prof main.py
