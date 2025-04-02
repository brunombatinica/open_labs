from manim import *
import numpy as np
from ipdb import set_trace as bp

class BaseScene(Scene):
    def setup(self):
        super().setup()
        # Set white background
        self.camera.background_color = WHITE

        self.x_range = [0, 8, 1]
        self.y_range = [0, 6, 1]
        
        # Create the axes
        self.axes = Axes(
            x_range=self.x_range,
            y_range=self.y_range,
            x_length=self.x_range[1] - self.x_range[0],
            y_length=self.y_range[1] - self.y_range[0],
            axis_config={
                "color": BLACK,
                "include_tip": True,
                "label_direction": DOWN,
            },
            x_axis_config={
                "numbers_to_include": [0, 2, 4, 6, 8],
            },
            y_axis_config={
                "numbers_to_include": [0, 2, 4, 6],
                "label_direction": LEFT,
            }
        )
        
        # Add axis labels
        self.x_label = Text("Weight", font_size=24, color=BLACK).next_to(self.axes.x_axis, DOWN*0.5)
        self.y_label = Text("Tail Length", font_size=24, color=BLACK).next_to(self.axes.y_axis, LEFT)
        
        # Group everything together
        self.axes_group = VGroup(self.axes, self.x_label, self.y_label)
        
        # Shift the entire coordinate system to center it
        # self.plot_shift = LEFT * 2 + DOWN * 1
        self.plot_shift = LEFT * 0 # no shift
        self.axes_group.shift(self.plot_shift)
        
        # Get the origin point (0,0) in screen coordinates
        self.origin = self.axes.c2p(0, 0)

        # Set random seed for reproducibility
        np.random.seed(273)
        
        # Store initial positions (above x-axis)
        self.initial_positions_blue = [
            self.axes.c2p(
                np.random.normal(2, 0.5),                 
                np.random.normal(3, 0.5)  
            )
            for _ in range(30)
        ]
        
        self.initial_positions_orange = [
            self.axes.c2p(
                np.random.normal(6, 0.5),                 
                np.random.normal(3, 0.5)  
            )
            for _ in range(30)
        ]

        # Create dots using stored positions
        self.initial_blue_dots = VGroup(*[
            Dot(
                color="#562C0C",
                # stroke_color=BLACK,
                # stroke_width=2
                ).move_to(pos)            
            for pos in self.initial_positions_blue
        ])

        self.initial_orange_dots = VGroup(*[
            Dot(color="#F5A739",
                # stroke_color=BLACK,
                # stroke_width=2
                ).move_to(pos)
            for pos in self.initial_positions_orange
        ])

        xy_coordinates_blue = [
            (np.clip(np.random.normal(3.2, 1), self.x_range[0], self.x_range[1] - 0.8), np.clip(np.random.normal(2, 0.7), self.y_range[0], self.y_range[1] - 0.5)) 
            for _ in range(30)]
        xy_coordinates_orange = [
            (np.clip(np.random.normal(5, 1), self.x_range[0], self.x_range[1] - 0.8), np.clip(np.random.normal(4, 0.6), self.y_range[0], self.y_range[1] - 0.5)) 
            for _ in range(30)]


        self.x_positions_blue = [self.axes.c2p(xy[0], 0) for xy in xy_coordinates_blue]
        self.x_positions_orange = [self.axes.c2p(xy[0], 0) for xy in xy_coordinates_orange]

        self.x_blue_dots = VGroup(*[
            Dot(color="#562C0C").move_to(pos)
            for pos in self.x_positions_blue
        ])

        self.x_orange_dots = VGroup(*[
            Dot(color="#F5A739").move_to(pos)
            for pos in self.x_positions_orange
        ])

        self.xy_positions_blue = [self.axes.c2p(xy[0], xy[1]) for xy in xy_coordinates_blue]
        self.xy_positions_orange = [self.axes.c2p(xy[0], xy[1]) for xy in xy_coordinates_orange]

class RandomDots(BaseScene):
    def construct(self):
        self.play(Create(self.initial_blue_dots), Create(self.initial_orange_dots))
        self.wait(2)

class ShowXAxis(BaseScene):
    def construct(self):
        # Add dots from previous scene
        self.add(self.initial_blue_dots, self.initial_orange_dots)
        self.wait()
        
        # Show x-axis and its label
        self.play(
            Create(self.axes.x_axis),
            Create(self.x_label)
        )
        self.wait(2)

class MoveDots1D(BaseScene):
    def construct(self):
        # Add elements from previous scene
        self.add(self.initial_blue_dots, self.initial_orange_dots, self.axes.x_axis, self.x_label)
        self.wait()

        # Set seed for consistent final positions
        np.random.seed(42)

        self.play(
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.initial_blue_dots, self.x_positions_blue)
            ],
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.initial_orange_dots, self.x_positions_orange)
            ],
            run_time=2
        )
        self.wait(2)

class ShowYAxis(BaseScene):
    def construct(self):
        # Add elements from previous scene
        self.add(self.x_blue_dots, self.x_orange_dots, self.axes.x_axis, self.x_label)
        
        self.play(
            Create(self.axes.y_axis),
            Create(self.y_label)
        )
        self.wait(2)

class MoveDots2D(BaseScene):
    def construct(self):
        # Add all elements from previous scene
        self.add(self.x_blue_dots, self.x_orange_dots, self.axes_group)
        
        # Set seed for consistent positions
        np.random.seed(42)
        
        # Move dots to their 2D positions
        self.play(
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.x_blue_dots, self.xy_positions_blue)
            ],
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.x_orange_dots, self.xy_positions_orange)
            ],
            run_time=2
        )
        self.wait(2) 