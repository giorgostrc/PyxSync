import pytest

from main import get_camera_model


@pytest.mark.parametrize(
    "filepath, exp_result",
    [
        ("./images/test_img_01.NEF", "NIKON D200"),
        ("./images/test_img_02.ARW", "SONY NEX-5"),
    ],
)
def test_get_camera_model(filepath, exp_result):
    model = get_camera_model(filepath)
    assert model == exp_result
