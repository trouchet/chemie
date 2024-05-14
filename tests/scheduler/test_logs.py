import pytest
from pathlib import Path
import os
from time import time

from backend.app.api.constants import MAX_LOG_FILES, MAX_LOG_FOLDER_SIZE_MB
from backend.app.scheduler.tasks.logs_clean_task import (
    get_files_sorted_by_mtime, 
    manage_files, 
    manage_files_periodically
)
from tests.conftest import clean_directory

def test_get_files_sorted_by_mtime_empty_dir(directory):
    """
    Test get_files_sorted_by_mtime with an empty directory.
    """
    files = get_files_sorted_by_mtime(str(directory))
    assert files == []
    
    clean_directory(directory)


def test_get_files_sorted_by_mtime_multiple_files(directory):
    """
    Test get_files_sorted_by_mtime with multiple files (sorted by modification time).
    """
    
    file1 = directory / "file1.txt"
    file1.touch()
    file2 = directory / "file2.txt"
    
    # Adjust the time difference as needed
    later_mtime = time() + 10   

    # Set a later modification time
    os.utime(file2, (later_mtime, later_mtime)) 

    files = get_files_sorted_by_mtime(str(directory))
    assert len(files) == 2
    
    # Modification time of first file should be earlier
    assert files[0][0] < files[1][0]
    
    # First element should be the path to file1
    assert files[0][1] == file1
    
    clean_directory(directory)


def test_manage_files_no_deletion(directory):
    """
    Test manage_files with no files exceeding limits.
    """
    
    file1 = directory / "file1.txt"
    file1.touch()
    file1.write_text("This is a test file")

    manage_files(str(directory))

    # Check that the file still exists
    assert file1.exists()
    
    clean_directory(directory)
    

def test_manage_files_delete_by_count(directory):
    """
    Test manage_files that deletes the oldest file when exceeding the file count limit.
    """
    
    file1 = directory / "file1.txt"
    file1.touch()
    file2 = directory / "file2.txt"
    file2.touch()
    file3 = directory / "file3.txt"
    file3.touch()
    print(directory)
    manage_files(str(directory), max_files=2)
    
    # Check that only two files remain
    assert len(list(directory.iterdir())) == 2

    # Check that the oldest file (file1) is deleted
    assert not file1.exists()
    
    clean_directory(directory)


def test_manage_files_delete_by_size(directory):
    """
    Test manage_files that deletes files until the total size limit is met.
    """
    file1 = directory / "file1.txt"
    file1.write_text("This is a large file" * 10)
    
    filepath=str(directory)
    manage_files(filepath, max_size_mb=1)

    # Check that the file is deleted
    assert not file1.exists()

    clean_directory(directory)

