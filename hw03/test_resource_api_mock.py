from unittest.mock import MagicMock
import main_resource_api as res_app


def test_list_contents_uses_bucket_objects_filter(monkeypatch):
    fake_bucket = MagicMock()
    fake_bucket.objects.filter.return_value = [MagicMock(key="k1"), MagicMock(key="k2")]

    fake_resource = MagicMock()
    fake_resource.Bucket.return_value = fake_bucket
    monkeypatch.setattr(res_app, "s3_resource", fake_resource)

    out = res_app.list_contents("b", "test/")
    fake_resource.Bucket.assert_called_once_with("b")
    fake_bucket.objects.filter.assert_called_once_with(Prefix="test/")
    assert out == ["k1", "k2"]


def test_get_file_uses_object(monkeypatch):
    fake_obj = MagicMock()
    fake_obj.get.return_value = {"Body": MagicMock(read=MagicMock(return_value=b"hi"))}

    fake_resource = MagicMock()
    fake_resource.Object.return_value = fake_obj
    monkeypatch.setattr(res_app, "s3_resource", fake_resource)

    data = res_app.get_file("b", "folder", "f.txt")
    fake_resource.Object.assert_called_once_with("b", "folder/f.txt")
    assert data == b"hi"
