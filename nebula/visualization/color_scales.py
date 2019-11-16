from typing import Sequence
from colour import Color


class ColorScale:
    _min_color = Color('#df9bec')
    _max_color = Color('#40044b')

    def __init__(self, ticks: Sequence[float]):
        self.size = len(ticks)
        self.colors = [
            c.hex for c in
            self._min_color.range_to(self._max_color, self.size)
        ]
        self.min_tick = min(ticks)
        self.max_tick = max(ticks)

    def __getitem__(self, tick: float) -> str:
        return self.colors[round(
            (self.size - 1) *
            (tick - self.min_tick) /
            (self.max_tick - self.min_tick)
        )]
