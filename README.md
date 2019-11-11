# dm-code-challenge

## Summary
This script generates a pie chart of `VISCODE` counts from Registry data and generates a CSV file from Registry and EC data filtered.

### Specification Notes
- Pie chart is hard filtered to `SVPERF` is 'Y' and `VISCODE` is not 'bl'
- CSV is hard named `results.csv`
- CSV results are filtered to include only one `VISCODE`, include only one `SVDOSE`, and exclude one `ECSDSTXT`
- CSV default filters to where `VISCODE` is 'w02', `SVDOSE` is 'Y', and `ECSDSTXT` is not 280

### Assumptions for Challenge
- Input CSVs are static and therefore filenames are hardcoded here
- `VISCODE` and `SVDOSE` are strings, `ECSDSTXT` is numeric, and therefore datatypes are not validated

## Setup
First clone the repository. In terminal run the following.
```sh
git clone git@github.com:dichuuu/dm-code-challenge.git
cd dm-code-challenge/
```

> If you do not have git, you can manually download the files
  
The following assumes you are in a directory with all the files. Activate a virtual environment now if you'd like. Then install dependencies.
  
```sh
pip install -r requirements.txt
```

## Script
To run the script with default filter parameters, run the following. 
```sh
python dosing.py
```
> Note that this may overwrite `results.csv`

The filters viscode, svdose, and ecsdstxt are optional parameters. The path for the output `results.csv` is an optional parameter as well. The following is an example.
```sh
python dosing.py --viscode w02 --svdose Y --ecsdstxt 280 --path results/
```
> Please ensure that the path is valid (in this example results/ should exist in this directory)


For more information, you can run
```sh
python dosing.py -h
```

## Tests
There are tests to ensure CSV generation logic is correct. To run tests, in the same directory, use the following command.
```sh
pytest
```
> Note that in Python 3 there is a warning for pytest but the tests are correct
