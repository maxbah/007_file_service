import pytest

from src import file_service
from mock import mock_open
import mock


def test_create_file_success(mocker):
    """
    Test create file positive
    :param mocker: mock object
    :return: none
    """
    mocked_open = mock_open()
    mocker.patch("builtins.open", mocked_open, create=True)
    test_file_name = "test_random_string"
    mocker.patch("src.utils.random_file_name").return_value = test_file_name

    file_service.create("blabla")

    mocked_open.assert_called_with(test_file_name, "w")
    mocked_open().write.assert_called_with("blabla")


def test_create_file_duplicate(mocker):
    """
    Test to check file duplicates
    :param mocker: mock object
    :return: None
    """
    mocked_open = mock_open()
    mocker.patch("builtins.open", mocked_open, create=True)
    test_filename = 'test_rand_string'
    second_test_filename = 'second_test_rand_string'

    path_exist_mock = mocker.patch('os.path.exists')

    path_exist_call_count = 0

    def on_path_exist_call(filename: str) -> bool:
        """
        Func to check path exists
        :param filename: Name of file
        :return: Bool
        """
        nonlocal path_exist_call_count
        path_exist_call_count += 1
        if path_exist_call_count == 1:
            assert filename == test_filename
            return True

        assert filename == second_test_filename
        return False

    path_exist_mock.side_effect = on_path_exist_call
    rand_string_mock = mocker.patch('src.utils.random_file_name')

    def random_string_side_effect() -> str:
        """
        Side effect for random string
        :return: str
        """
        if len(rand_string_mock.mock_calls) == 1:
            return test_filename
        return second_test_filename
    rand_string_mock.side_effect = random_string_side_effect

    file_service.create("blabla")

    assert path_exist_mock.mock_calls == [mock.call(test_filename), mock.call(second_test_filename)]
    mocked_open.assert_called_with(second_test_filename, 'w')
    mocked_open().write.assert_called_with("blabla")


def test_delete_file(mocker):
    """
    Test to check file delete
    :param mocker: mock object
    :return: none
    """
    del_file_mock = mocker.patch("os.remove")
    test_filename = 'test_rand_string'
    file_service.delete_file(test_filename)
    del_file_mock.assert_called_with(test_filename)


def test_list_dir(mocker):
    """
    Test to check list directory
    :param mocker: mock object
    :return: None
    """
    list_dir_mock = mocker.patch("os.listdir")
    list_dir_mock.return_value = ["a"]
    res = file_service.list_dir('./')
    list_dir_mock.assert_called_once()
    assert res == ["a"]


def test_change_dir_success_flow(mocker):
    """
    Test to change directory positive
    :param mocker: mock obj
    :return: None
    """
    ch_dir_mock = mocker.patch("os.chdir")
    targ_dir = './'
    file_service.change_dir(targ_dir)
    ch_dir_mock.assert_called_with(targ_dir)


def test_change_dir_not_exist(mocker):
    """
    Test to check change dir bot existed
    :param mocker: mock object
    :return: None
    """
    ch_dir_mock = mocker.patch("os.chdir")
    targ_dir = 'test_dir'
    ch_dir_mock.return_value = 'FileNotFoundError'
    with pytest.raises(Exception):
        raise file_service.change_dir(targ_dir)


def test_get_metadata(mocker):
    """
    Test for check metadata for filename
    :param mocker: mock object
    :return: None
    """
    test_filename = 'test_file'
    get_metadata_mock = mocker.patch('src.file_service.get_file_metadata')
    get_metadata_mock.return_value = ('Jan 01 1970 02:07:36', 'Jan 01 1970 02:07:36', 789)

    create_date_mock = mocker.patch('src.utils.get_human_date')
    create_date_mock.return_value = 'Jan 01 1970 02:07:36'
    file_size_mock = mocker.patch('os.path.getsize')
    file_size_mock.return_value = 789

    res = file_service.get_file_metadata(test_filename)

    get_metadata_mock.assert_called_with(test_filename)
    assert res == ('Jan 01 1970 02:07:36', 'Jan 01 1970 02:07:36', 789)


def test_non_existing_file_metadata(mocker):
    """
    Test metadata for non existing file
    :param mocker: mock obj
    :return: None
    """
    test_filename = 'test_file'
    exist_mock = mocker.patch('os.path.exists')
    exist_mock.return_value = 'FileNotFoundError'
    with pytest.raises(Exception):
        raise file_service.get_file_metadata(test_filename)
