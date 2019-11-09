from typing import Sequence
from colour import Color
from math import isclose
from nebula.utils import find


class ColorScale:
    min_color = Color('#df9bec')
    max_color = Color('#40044b')

    def __init__(self, tickles: Sequence[float]):
        self._tickles = sorted(tickles)
        self._colors = list(self.min_color.range_to(self.max_color, len(tickles)))

    def __getitem__(self, value: float) -> str:
        return find(
            lambda p: value < p[0] or isclose(value, p[0]),
            zip(self._tickles, self._colors),
            (0, self.max_color)
        )[1].hex
