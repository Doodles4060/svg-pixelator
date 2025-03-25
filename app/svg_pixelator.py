import pathlib
from typing import Union, IO, Tuple

import matplotlib.pyplot as plt
import numpy as np
import svgpathtools
from numpy.typing import NDArray

from settings import TEST_IMAGE_ROOT, TEST_FILES, IMAGE_ROOT


class SVGPixelator:
    file: IO
    path: Union[pathlib.Path, str]
    aspect_ratio: Tuple[int, int]
    pixelation_level: int

    _invalid_ratio_msg = 'Invalid ratio format!'
    _default_ratio = (5, 5)

    def __init__(self, file: IO, path: Union[pathlib.Path, str],
                 aspect_ratio: Union[str, None], pixelation_level: int) -> None:
        self.file = file
        self.path = path
        self.aspect_ratio = self.parse_aspect_ratio(aspect_ratio)
        self.pixelation_level = pixelation_level

    def parse_aspect_ratio(self, _aspect_ratio: str) -> Tuple[int, int]:
        if not ':' in _aspect_ratio and not '/' in _aspect_ratio:
            return self._default_ratio

        ratios = []
        if ':' in _aspect_ratio:
            ratios = _aspect_ratio.split(':')
        elif '/' in _aspect_ratio:
            ratios = _aspect_ratio.split('/')

        try:
            return int(ratios[0]), int(ratios[1])
        except ValueError:
            return self._default_ratio

    def extract_all_paths(self, num_samples=1000) -> NDArray[np.float64]:
        """Extracts all path elements and converts them to a single NumPy array of points."""
        paths, _ = svgpathtools.svg2paths(self.file)

        all_points = []
        for path in paths:
            for segment in path:
                for t in np.linspace(0, 1, num_samples):
                    point = segment.point(t)
                    all_points.append((point.real, point.imag))

        return np.array(all_points)

    @staticmethod
    def snap_to_grid(points: NDArray[np.float64], pixel_size: Union[int, float] = 10) -> NDArray[np.float64]:
        """Snap a set of points to a pixel grid."""
        snapped = np.unique(np.round(points / pixel_size) * pixel_size, axis=0)
        snapped[:, 1] *= -1  # Flip Y-axis
        return snapped

    @staticmethod
    def clean_plot() -> None:
        plt.axis("off")
        plt.gca().set_xticks([])
        plt.gca().set_yticks([])
        plt.gca().set_frame_on(False)

    def build_and_save_plot(self, _original_points: NDArray[np.float64],
                            _pixelated_points: NDArray[np.float64]) -> None:
        """Plot original and pixelated points for visualization."""
        plt.figure(figsize=self.aspect_ratio)
        self.clean_plot()

        plt.scatter(_pixelated_points[:, 0], -_pixelated_points[:, 1], s=10, c='black')
        plt.savefig(str(self.path) + '.png', format="png", bbox_inches="tight", pad_inches=0)
        plt.close()

    def get_final_image(self) -> None:
        original_points = self.extract_all_paths(num_samples=500)
        pixelated_points = self.snap_to_grid(original_points, pixel_size=self.pixelation_level)

        self.build_and_save_plot(original_points, pixelated_points)


if __name__ == '__main__':
    test_file = TEST_IMAGE_ROOT / TEST_FILES['LARGE']

    with open(test_file, 'r') as f:
        file_name = f.name.split('.')[0].split('\\')[-1]
        save_path = IMAGE_ROOT / file_name
        pixelator = SVGPixelator(f, IMAGE_ROOT / file_name, '30:20', 50)
        pixelator.get_final_image()
