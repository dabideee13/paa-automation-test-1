import shutil
import glob
import os
from pathlib import Path
from typing import Union

import pandas as pd

from tools import get_config


def get_file(domain: str, filename: str) -> Path:
    return Path.joinpath(Path(get_config(domain)['download_path']), filename)


def clean_counts(counts: Union[str, int]) -> int:
    counts = str(counts).strip().replace(',', '')
    return int(counts) if counts else 0


def add_inventory(location1_inventory: int, location2_inventory: int) -> int:
    if location1_inventory < 0:
        location1_inventory = 0
    if location2_inventory < 0:
        location2_inventory = 0

    return location1_inventory + location2_inventory


def add_path(path, file):
    return str(Path.joinpath(path, file))


if __name__ == '__main__':

    webfront_config = get_config('webfront')
    retail_deck_config = get_config('retail_deck')
    portal_config = get_config('portal')

    webfront_path = webfront_config['download_path']
    portal_path = portal_config['download_path']
    retail_deck_path = retail_deck_config['download_path']
    download_path = Path.joinpath(Path.cwd(), 'data', 'downloads')

    webfront_filename = [file for file in os.listdir(webfront_path) if file != '.DS_Store'][0]
    retail_deck_filename = [file for file in os.listdir(retail_deck_path) if file != '.DS_Store'][0]
    portal_filename = [file for file in os.listdir(portal_path) if file != '.DS_Store'][0]

    webfront_file = add_path(Path(webfront_path), webfront_filename)
    retail_deck_file = add_path(Path(retail_deck_path), retail_deck_filename)
    print(retail_deck_file)
    portal_file = add_path(Path(portal_path), portal_filename)

    shutil.move(webfront_file, download_path)
    shutil.move(retail_deck_file, download_path)
    shutil.move(portal_file, download_path)

    webfront_file = Path.joinpath(download_path, webfront_filename)
    retail_deck_file = Path.joinpath(download_path, retail_deck_filename)
    portal_file = Path.joinpath(download_path, portal_filename)

    retail_deck_data = pd.read_csv(retail_deck_file)
    webfront_data = pd.read_csv(webfront_file)
    portal_data = pd.read_csv(portal_file)

    # Groupby data
    retail_deck_data['Medford'] = retail_deck_data['Medford'].apply(clean_counts)
    retail_deck_data['NJ'] = retail_deck_data['NJ'].apply(clean_counts)
    retail_deck_data['INVENTORY'] = (
        retail_deck_data[['Medford', 'NJ']]
        .apply(lambda x: add_inventory(x['Medford'], x['NJ']), axis=1)
    )

    webfront_data['Medford (PARKAVEAPPL)'] = webfront_data['Medford (PARKAVEAPPL)'].apply(clean_counts)
    webfront_data['NJ (PARKAVEAPPL)'] = webfront_data['NJ (PARKAVEAPPL)'].apply(clean_counts)
    webfront_data['INVENTORY'] = (
        webfront_data[['Medford (PARKAVEAPPL)', 'NJ (PARKAVEAPPL)']]
        .apply(lambda x: add_inventory(x['Medford (PARKAVEAPPL)'], x['NJ (PARKAVEAPPL)']), axis=1)
    )

    data1 = retail_deck_data[['PN', 'INVENTORY']]
    data2 = webfront_data[['PN', 'INVENTORY']]
    data3 = portal_data[['Model Number', 'Committed']]

    data3.columns = ['PN', 'INVENTORY']

    all_data = pd.concat([data1, data2, data3]).reset_index(drop=True)
    all_data.groupby('PN').count().reset_index()

    all_data.to_csv(
        Path.joinpath(
            get_config()['general']['download_path'],
            'data.csv'
        ),
        index=False
    )



