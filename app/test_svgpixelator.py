from unittest import TestCase

from svg_pixelator import SVGPixelator
from settings import TEST_IMAGE_ROOT, TEST_FILES, IMAGE_ROOT

test_file = TEST_IMAGE_ROOT / TEST_FILES['MEDIUM']

class TestSVGPixelator(TestCase):
    _pixelator = SVGPixelator(test_file, IMAGE_ROOT, '16:9', 10)

    def test_aspect_ratio_parser(self):
        result = self._pixelator.parse_aspect_ratio('16/9')
        print(result)
        self.assertEqual(result, (16, 9))