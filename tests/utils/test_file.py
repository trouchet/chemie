import os
from pathlib import Path
import pytest
from shutil import rmtree

from backend.app.api.utils.file import (
    get_filename,
    extend_filename,
    create_folder,
    get_file_size,
)


def test_get_filename_with_extension():
    """Test get_filename with a filename containing an extension."""
    filename = "file.txt"
    extracted_filename = get_filename(filename)
    assert extracted_filename == "file.txt"


def test_get_filename_without_extension():
    """Test get_filename with a filename without an extension."""
    filename = "nofileextension"
    extracted_filename = get_filename(filename)
    assert extracted_filename == "nofileextension"


def test_get_filename_with_path():
    """Test get_filename with a path containing the filename."""
    filename = "/path/to/my/file.txt"
    extracted_filename = get_filename(filename)
    assert extracted_filename == "file.txt"


def test_extend_filename_simple():
    """Test extend_filename with a simple token."""
    filename = "image.jpg"
    new_filename = extend_filename(filename, "resized")
    assert new_filename == "image_resized.jpg"


def test_extend_filename_custom_delimiter():
    """Test extend_filename with a custom delimiter."""
    filename = "data_file"
    new_filename = extend_filename(filename, "encrypted", "_")
    assert new_filename == "data_encrypted_file"


def test_extend_filename_no_extension():
    """Test extend_filename with a filename without an extension."""
    filename = "nofileextension"
    new_filename = extend_filename(filename, "extended")
    assert new_filename == "nofileextension_extended"


def test_create_folder_existing_folder(tmp_path):
    """Test create_folder with an existing directory."""
    directory_name = str(tmp_path / "existing_folder")
    os.makedirs(directory_name)

    create_folder(directory_name)

    # Simulate checking the printed message (replace with actual printing assertion if needed)
    assert f"Directory '{directory_name}' already exists." in capture_messages(create_folder, directory_name)


def test_create_folder_new_folder(tmp_path):
    """Test create_folder with a new directory."""
    directory_name = str(tmp_path / "new_folder")
    rmtree(str(directory_name))
    create_folder(directory_name)

    # Simulate checking the printed message (replace with actual printing assertion if needed)
    assert f"Directory '{directory_name}' created!" in capture_messages(create_folder, directory_name)


def test_get_file_size_existing_file(tmp_path):
    """Test get_file_size with an existing file."""
    file_path = tmp_path / "test_file.txt"
    with open(file_path, "w") as f:
        f.write("This is some test content")

    file_size = get_file_size(str(file_path))
    assert isinstance(file_size, int) and file_size > 0


def test_get_file_size_non_existent_file(tmp_path):
    """Test get_file_size with a non-existent file."""
    file_path = str(tmp_path / "non_existent_file.txt")

    with pytest.raises(FileNotFoundError) as excinfo:
        get_file_size(file_path)

    assert "File not found" in str(excinfo.value) and file_path in str(excinfo.value)


# Helper function to capture printed messages during test execution
def capture_messages(func, *args, **kwargs):
    import contextlib
    import io

    with contextlib.redirect_stdout(io.StringIO()) as f:
        func(*args, **kwargs)
    return f.getvalue()
