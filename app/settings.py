import pathlib

"""Root directory of the project"""
BASE_DIR = pathlib.Path(__file__).parent.resolve()

"""
Root folder for .svg image files
"""
IMAGE_ROOT = BASE_DIR / 'img'

"""
Image folder for testing
"""
TEST_IMAGE_ROOT = BASE_DIR / 'test_img'
TEST_FILES = {
    'SMALL': 'small.svg',
    'MEDIUM': 'medium.svg',
    'LARGE': 'large.svg',
}