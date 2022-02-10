from src import utils


def test_random_file_name(mocker):
    """
    Test to check random file name
    :param mocker: mock obj
    :return: None
    """
    test_file_name = "test_random_string"
    test_f_name = mocker.patch("src.utils.random_file_name").return_value = test_file_name
    count = 0
    while count <= 1000:
        count += 1
        assert utils.random_file_name() == test_f_name


def test_human_date(mocker):
    """
    Test for check human date
    :param mocker: mock obj
    :return: None
    """
    test_date = 1643885546.389199
    hum_date_mock = mocker.patch("src.utils.get_human_date")
    hum_date_mock.return_value = 'Feb 03 2022 12:52:26'

    res = utils.get_human_date(test_date)

    hum_date_mock.assert_called_with(test_date)
    assert res == 'Feb 03 2022 12:52:26'

