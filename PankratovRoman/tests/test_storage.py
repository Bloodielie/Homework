import tempfile

from rss_parser.storage import FileStorage


def test_file_storage():
    temp_file_path = tempfile.mkstemp()[1]

    file_storage = FileStorage(temp_file_path)
    assert file_storage.data == {}

    file_storage["1"] = 1

    file_storage.save()
    file_storage.close()

    with open(temp_file_path) as f:
        assert f.read() == '{"1": 1}'
