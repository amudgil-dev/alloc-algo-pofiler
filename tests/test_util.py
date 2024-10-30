import pytest
from datetime import datetime
from app.utils.util import Util, FileUtil, NumpyEncoder
import json
import numpy as np
import logging


def test_generate_filename_prefix_and_extension():
    result = Util.generate_filename("testfile", "txt")
    # print(" ---- ", result)
    assert result.startswith("testfile_"), "Filename should start with the given prefix"
    assert result.endswith(".txt"), "Filename should end with the given extension"


def test_generate_filename_timestamp_format():
    result = Util.generate_filename("test", "csv")

    timestamp_part = result[5:-4]  # Extract the timestamp part
    assert (
        len(timestamp_part) == 15
    ), "Timestamp should be 15 characters long (including underscore)"
    assert (
        timestamp_part[8] == "_"
    ), "Timestamp should have an underscore at the 9th position"

    # Check if the timestamp part can be parsed as a valid datetime
    try:
        datetime.strptime(timestamp_part, "%Y%m%d_%H%M%S")
    except ValueError:
        pytest.fail("Timestamp part is not in the correct format")


def test_generate_filename_uniqueness():
    result1 = Util.generate_filename("test", "txt")
    result2 = Util.generate_filename("test", "json")
    assert result1 != result2, "Generated filenames should be unique"


def test_numpy_encoder():
    encoder = NumpyEncoder()

    # Test integer conversion
    assert encoder.default(np.int64(10)) == 10
    assert encoder.default(np.int32(20)) == 20

    # Test float conversion
    assert encoder.default(np.float64(10.5)) == 10.5
    assert encoder.default(np.float32(20.5)) == 20.5

    # Test ndarray conversion
    arr = np.array([1, 2, 3])
    assert encoder.default(arr) == [1, 2, 3]

    # Test default case with unsupported type
    with pytest.raises(TypeError):
        encoder.default(object())


def test_save_as_json(tmp_path, caplog):
    # Test with regular Python types
    data = {"a": 1, "b": 2, "c": [3, 4, 5]}
    filename = tmp_path / "test_regular.json"
    FileUtil.save_as_json(data, filename)

    with open(filename, "r") as f:
        loaded_data = json.load(f)
    assert loaded_data == data

    # Test with numpy types
    np_data = {
        "int": np.int64(10),
        "float": np.float32(20.5),
        "array": np.array([1, 2, 3]),
    }
    filename = tmp_path / "test_numpy.json"
    FileUtil.save_as_json(np_data, filename)

    with open(filename, "r") as f:
        loaded_np_data = json.load(f)
    assert loaded_np_data == {"int": 10, "float": 20.5, "array": [1, 2, 3]}

    # Test with unsupported type

    # caplog.set_level(logging.WARNING)  # Ensure we capture warning messages

    # # Test with unsupported type
    # unsupported_data = {
    #     "supported": 42,
    #     "unsupported": object(),
    #     "nested": {"good": [1, 2, 3], "bad": set()},
    # }
    # filename = tmp_path / "test_unsupported.json"

    # cleaned_data = FileUtil.save_as_json(unsupported_data, filename)

    # assert "Some data was removed due to serialization issues." in caplog.text
    # assert "Removed non-serializable item: <class 'object'>" in caplog.text
    # assert "Removed non-serializable item: <class 'set'>" in caplog.text

    # expected_cleaned_data = {"supported": 42, "nested": {"good": [1, 2, 3]}}
    # assert cleaned_data == expected_cleaned_data

    # with open(filename, "r") as f:
    #     loaded_data = json.load(f)

    # assert loaded_data == expected_cleaned_data
