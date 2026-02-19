from unittest.mock import MagicMock
import main_client_api as client_app


def test_list_contents_calls_list_objects_v2(monkeypatch):
    fake_client = MagicMock()
    fake_client.list_objects_v2.return_value = {
        "Contents": [{"Key": "a.txt"}, {"Key": "b.txt"}]
    }
    monkeypatch.setattr(client_app, "s3_client", fake_client)

    out = client_app.list_contents("my-bucket", "folder/")
    fake_client.list_objects_v2.assert_called_once_with(
        Bucket="my-bucket", Prefix="folder/"
    )
    assert out == ["a.txt", "b.txt"]


def test_get_file_calls_get_object(monkeypatch):
    fake_body = MagicMock()
    fake_body.read.return_value = b"data"
    fake_client = MagicMock()
    fake_client.get_object.return_value = {"Body": fake_body}
    monkeypatch.setattr(client_app, "s3_client", fake_client)

    data = client_app.get_file("my-bucket", "folder", "x.txt")
    fake_client.get_object.assert_called_once_with(
        Bucket="my-bucket", Key="folder/x.txt"
    )
    assert data == b"data"
