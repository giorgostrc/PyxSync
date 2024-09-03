import os

import pytest

from app.processing import get_camera_model

basedir = os.path.dirname(__file__)


@pytest.mark.parametrize(
    "filepath, exp_result",
    [
        (os.path.join(basedir, "images/test_img_01.NEF"), "NIKON D200"),
        (os.path.join(basedir, "images/test_img_02.ARW"), "SONY NEX-5"),
    ],
)
def test_get_camera_model(filepath, exp_result):
    model = get_camera_model(filepath)
    assert model == exp_result
