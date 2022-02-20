# MultiWOZ to Hindi translator

This python script is used to translate some parts of [MultiWOZ_2.1](https://github.com/budzianowski/multiwoz/tree/master/data "Available here") dataset after incorporating corrections from [MultiWOZ_2.2](https://github.com/budzianowski/multiwoz/tree/master/data/MultiWOZ_2.2 "Available here") to the Hindi language

Steps to incorporate **MultiWOZ_2.2** corrections into **MultiWOZ_2.1** dataset are available [here](https://github.com/budzianowski/multiwoz/tree/master/data/MultiWOZ_2.2#conversion-to-the-data-format-of-multiwoz-21).

## Requirements
- `python 3.8.5` with `pandas 1.2.0`
- Segregated MultiWOZ dataset from [multiwoz-segregate](https://github.com/calm-cookie/multiwoz-segregate).
- Database file with hindi keywords (confidential).

## How to Run
Preliminary Steps
- Install **pandas** using  `pip3 install pandas==1.2.0`
- Go to `hindi.py` and set `ATTRACTION_EXCEL`, `OUTPUT_DIR`, `DATASET_DIR` paths in _line 21 -23_. By default, the directories are set to the current directory.

Final Step
- `python3 hindi.py`

## Output
- `JSON` files from dataset with replaced user dialog-acts in `hindi-dataset/attraction-restaurant-taxi`
- `hindi-dataset/not_found_attraction_hindi.json` with values that were not matched in database (hindi equivalent not found)
