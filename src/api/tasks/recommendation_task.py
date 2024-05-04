from os import listdir, path, getcwd

from src.api.setup.logging import logger
from src.api.utils.dataframe import read_data_from_file

# NOTE: The columns are hardcoded for now
dataset_columns = [
    'itemset_timestamp',
    'itemset_id',
    'agent_id',
    'item_id',
    'item_description',
    'item_quantity',
    'item_value',
]


def generate_recommendations():
    logger.debug("Scheduled task: Generating recommendations...")
    data_path = path.join(getcwd(), 'data')

    files_list = listdir(data_path)

    for file in files_list:
        try:
            filepath = path.join(data_path, file)

            read_data_from_file(filepath, dataset_columns)

        except ValueError:
            continue

    for file in files_list:
        logger.debug(f"Processing file: {file}")
