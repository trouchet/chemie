import pytest
import pandas as pd
from unittest.mock import patch
from src.utils.dataframe import (
    listify_items,
    get_descriptions,
    get_years,
    get_unique_elements,
    read_data_from_file,
    read_data_to_dataframe_gen,
    read_data_to_dataframe
)
from os import path
import pandas as pd

def test_read_data_to_dataframe_gen(tmpdir):
    # Create a temporary directory and some test Excel files
    data_folder = tmpdir.mkdir("data")
    file1 = data_folder.join("file1.xlsx")
    file2 = data_folder.join("file2.xlsx")

    # Write some test data to the Excel files
    data1 = {"sets_column": [1, 2, 3], "items_column": ['a', 'b', 'c']}
    data2 = {"sets_column": [4, 5, 6], "items_column": ['d', 'e', 'f']}
    pd.DataFrame(data1).to_excel(file1, index=False)
    pd.DataFrame(data2).to_excel(file2, index=False)

    # Test the function
    results = list(read_data_to_dataframe_gen(str(data_folder), "sets_column", "items_column"))

    # Check if the results are as expected
    assert len(results) == 2
    for filepath, df_ in results:
        assert path.exists(filepath)
        assert isinstance(df_, pd.DataFrame)
        assert "sets_column" in df_.columns
        assert "items_column" in df_.columns

def test_listify_items(sample_df):
    expected_result = [['a', 'b'], ['c', 'd'], ['e', 'f']]
    result = listify_items(sample_df, 'sets_column', 'items_column')
    assert result == expected_result

def test_get_descriptions(sample_df):
    expected_result = {
        'a': 'desc_a', 
        'b': 'desc_b', 
        'c': 'desc_c', 
        'd': 'desc_d', 
        'e': 'desc_e', 
        'f': 'desc_f'
    }

    result = get_descriptions(sample_df, 'items_column', 'description_column')
    
    assert result == expected_result

def test_get_years(sample_df):
    expected_result = [2022, 2023, 2024]
    result = get_years(sample_df, 'date_column')
    assert result == expected_result

def test_get_unique_elements(sample_df):
    expected_result = ['a', 'b', 'c', 'd', 'e', 'f']
    result = get_unique_elements(sample_df, 'items_column')
    assert result == expected_result

def test_read_data_from_file(sample_df):
    filepath = 'sample_file.xlsx'
    sets_column = 'sets_column'
    items_column = 'items_column'
    
    with patch('pandas.read_excel') as mock_read_excel:
        mock_read_excel.return_value = sample_df
        result = read_data_from_file(filepath, sets_column, items_column)
    
    assert result.equals(sample_df)

def test_read_data_to_dataframe_gen_folder_not_found():
    with patch('os.listdir') as mock_listdir:
        mock_listdir.side_effect = FileNotFoundError
        data_folder = 'data_folder'
        sets_column = 'sets_column'
        items_column = 'items_column'
        extension = 'xlsx'
        
        gen = read_data_to_dataframe_gen(data_folder, sets_column, items_column, extension)
        with pytest.raises(FileNotFoundError):
            next(gen)

def test_read_data_to_dataframe(mock_read_data_to_dataframe_gen):
    data_folder = 'data_folder'
    sets_column = 'sets_column'
    items_column = 'items_column'
    extension = 'xlsx'

    # Call the function
    read_data_to_dataframe(data_folder, sets_column, items_column, extension)

    # Verify that read_data_to_dataframe_gen is called with the correct arguments
    mock_read_data_to_dataframe_gen.assert_called_once_with(data_folder, sets_column, items_column, extension)