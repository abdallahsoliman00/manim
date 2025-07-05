import numpy as np
from functools import lru_cache
from manimlib.mobject.types.vectorized_mobject import VMobject, VGroup
from manimlib.mobject.coordinate_systems import Axes
from manimlib.mobject.coordinate_systems import DEFAULT_X_RANGE, DEFAULT_Y_RANGE
from manimlib.constants import PI, UP, RIGHT, LEFT


def is_coordinate_pair(func_or_coords):
    try:
        x_coords, y_coords = func_or_coords
        # Try to get length - will work for lists, tuples, numpy arrays
        return len(x_coords) == len(y_coords) and len(x_coords) > 0
    except (TypeError, ValueError):
        return False


class Figure(VGroup):
    def __init__(
        self,
        func_or_coords,
        x_range = DEFAULT_X_RANGE,
        y_range = DEFAULT_Y_RANGE,
        width: float = 5,
        height: float = 5,
        allow_clip: bool = False,
        curve_stroke_config: dict = {
            'color': "#36E130",
            'width': 3,
            'opacity': 1
        },
        fit_axes_to_curve: bool = True,
        x_y_labels = None,
        num_points: int = 100,
        x_y_tick_freq = (1,1),
        axis_config: dict = {'include_numbers': False},
        x_axis_config: dict = dict(),
        y_axis_config: dict = {
                'line_to_number_direction': UP,
                'number_orientation' : -PI/2
        },
        **axis_config_kwargs
    ):
        super().__init__()

        self.x_range = x_range
        self.y_range = y_range

        self.curve = None
        self.axes_labels = None
        self.axes = None

        def call_axes_func(fitted: bool, x=None, y=None):
            ax_args = dict(
                x_range=x_range,
                y_range=y_range,
                width=width,
                height=height,
                axis_config=axis_config,
                x_axis_config=x_axis_config,
                y_axis_config=y_axis_config,
                **axis_config_kwargs
            )

            if fitted:
                max_x, min_x = np.max(x), np.min(x)
                max_y, min_y = np.max(y), np.min(y)
                ax_args['x_range'] = (min_x, max_x, x_y_tick_freq[0])
                ax_args['y_range'] = (min_y, max_y, x_y_tick_freq[1])

            self.create_axes(**ax_args)


        # Check if function or coodinates are valid, and create axes according to fit_axes_to_curve
        if func_or_coords is not None:
            if is_coordinate_pair(func_or_coords):
                if fit_axes_to_curve:
                    x,y = func_or_coords
                    call_axes_func(fitted=True, x=x, y=y)
                else:
                    call_axes_func(fitted=False)

                self.plot_from_coords(*func_or_coords, **curve_stroke_config)

            else:
                if fit_axes_to_curve:
                    x,y = self.get_points_from_func(func_or_coords, allow_clip=True, num_points=num_points)
                    call_axes_func(fitted=True, x=x, y=y)
                    self.plot_from_func(func_or_coords, allow_clip=True, num_points=num_points, **curve_stroke_config)

                else:
                    call_axes_func(fitted=False)
                    self.plot_from_func(func_or_coords, allow_clip=allow_clip, num_points=num_points, **curve_stroke_config)

        else: raise ValueError("argument func_or_coords requires a value. Cannot have an empty argument.")

        if x_y_labels is not None:
            self.add_axis_labels(*x_y_labels)

    
    def create_axes(
            self, x_range, y_range,
            width, height,
            axis_config, x_axis_config,
            y_axis_config, **axis_config_kwargs
        ):
        self.axes = Axes(
            x_range=x_range,
            y_range=y_range,
            width=width,
            height=height,
            axis_config=axis_config,
            x_axis_config=x_axis_config,
            y_axis_config=y_axis_config,
            **axis_config_kwargs
        )
        self.add(self.axes)

        
    def add_axis_labels(self, x_label, y_label):
        self.axes_labels = VGroup(
            self.axes.get_x_axis_label(x_label).shift(0.2*RIGHT),
            self.axes.get_y_axis_label(y_label).shift(UP*0.2 + 1.3*LEFT)
        )
        self.add(self.axes_labels)


    def remove_axes_labels(self):
        if self.axes_labels is not None:
            self.remove(self.axes_labels)

    
    @lru_cache
    def get_points_from_func(self, func, allow_clip=False, num_points=50):
        x = np.linspace(*self.x_range[:2], num_points)

        if allow_clip:
            y = func(x)
        else:
            y = np.array([func(i) if (self.axes.y_range[0] <= func(i) <= self.axes.y_range[1]) else np.nan for i in x])
            mask = ~np.isnan(y)
            x = x[mask]
            y = y[mask]

        return x,y


    def plot_from_func(self, func, allow_clip=False, num_points=50, **curve_stroke_config):
        x,y = self.get_points_from_func(func, allow_clip, num_points)

        if len(x) > 0:
            self.plot_from_coords(x, y, **curve_stroke_config)


    def plot_from_coords(self, x, y, **curve_stroke_config):
        if len(x) == 0 or len(y) == 0:
            return

        self.curve = VMobject()
        self.curve.set_points_smoothly(self.axes.c2p(x, y)).set_stroke(**curve_stroke_config)
        self.add(self.curve)
