from manim import *
import numpy as np

class BaseScene(Scene):
    def setup(self):
        super().setup()
        # Set white background
        self.camera.background_color = WHITE
        
        # Create the weight axis
        self.axis = NumberLine(
            x_range=[-4, 4, 1],
            length=8,
            include_tip=True,
            label_direction=DOWN,
            color=BLACK,
        )
        self.axis.add_labels({-4: "-4", -2: "-2", 0: "0", 2: "2", 4: "4"})
        self.axis_label = Text("Weight", font_size=24, color=BLACK).next_to(self.axis, DOWN)
        self.axis_group = VGroup(self.axis, self.axis_label)
        # Move axis group down
        self.axis_group.shift(DOWN * 2)

        # Set random seed for reproducibility
        np.random.seed(42)

        # Store initial positions
        self.initial_positions_blue = [
            np.array([
                np.random.uniform(-2, 2),
                np.random.uniform(0, 1),
                0
            ])
            for _ in range(30)
        ]
        
        self.initial_positions_orange = [
            np.array([
                np.random.uniform(-2, 2),
                np.random.uniform(0, 1),
                0
            ])
            for _ in range(30)
        ]

        # Create dots using stored positions
        self.blue_dots = VGroup(*[
            Dot(color=BLUE).move_to(pos)
            for pos in self.initial_positions_blue
        ])

        self.orange_dots = VGroup(*[
            Dot(color="#FFA500").move_to(pos)
            for pos in self.initial_positions_orange
        ])

class RandomDots(BaseScene):
    def construct(self):
        self.play(Create(self.blue_dots), Create(self.orange_dots))
        self.wait(2)

class ShowXAxis(BaseScene):
    def construct(self):
        self.add(self.blue_dots, self.orange_dots)
        self.wait()
        
        self.play(Create(self.axis_group))
        self.wait(2)

class MoveDots1D(BaseScene):
    def construct(self):
        self.add(self.blue_dots, self.orange_dots, self.axis_group)
        self.wait()

        # Set seed for consistent final positions
        np.random.seed(42)
        
        # Create final positions for normal distributions with more overlap
        blue_final_positions = [
            np.array([np.random.normal(-0.5, 0.8), -2, 0])
            for _ in range(30)
        ]
        orange_final_positions = [
            np.array([np.random.normal(0.5, 0.8), -2, 0])
            for _ in range(30)
        ]

        self.play(
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.blue_dots, blue_final_positions)
            ],
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.orange_dots, orange_final_positions)
            ],
            run_time=2
        )
        self.wait(2)

class ShowYAxis(BaseScene):
    def construct(self):
        # Add existing elements with dots in their 1D positions
        self.add(self.blue_dots, self.orange_dots, self.axis_group)
        
        # Get the origin position (left end of weight axis)
        origin = self.axis.number_to_point(self.axis.x_range[0])
        
        # Create vertical axis for tail length starting from origin
        y_axis = NumberLine(
            x_range=[0, 4, 1],  # Reduced range from 6 to 4
            length=6,  # Reduced length from 10 to 6
            include_tip=True,
            label_direction=RIGHT,
            color=BLACK,
        ).rotate(90 * DEGREES)
        
        # Position y-axis at origin
        y_axis.move_to(origin, aligned_edge=DOWN+LEFT)
        
        y_axis.add_labels({0: "0", 1: "1", 2: "2", 3: "3", 4: "4"})
        y_axis_label = Text("Tail Length", font_size=24, color=BLACK).next_to(y_axis, RIGHT)
        y_axis_group = VGroup(y_axis, y_axis_label)
        
        self.play(Create(y_axis_group))
        self.wait(2)

class MoveDots2D(BaseScene):
    def construct(self):
        # Add all existing elements including both axes
        self.add(self.blue_dots, self.orange_dots, self.axis_group)
        
        # Get the origin position
        origin = self.axis.number_to_point(self.axis.x_range[0])
        
        # Add y-axis (same as in ShowYAxis)
        y_axis = NumberLine(
            x_range=[0, 4, 1],  # Reduced range
            length=6,  # Reduced length
            include_tip=True,
            label_direction=RIGHT,
            color=BLACK,
        ).rotate(90 * DEGREES)
        y_axis.move_to(origin, aligned_edge=DOWN+LEFT)
        y_axis.add_labels({0: "0", 1: "1", 2: "2", 3: "3", 4: "4"})
        y_axis_label = Text("Tail Length", font_size=24, color=BLACK).next_to(y_axis, RIGHT)
        y_axis_group = VGroup(y_axis, y_axis_label)
        self.add(y_axis_group)
        
        # Set seed for consistent positions
        np.random.seed(42)
        
        # Create final 2D positions
        blue_final_positions = [
            np.array([
                np.random.normal(-0.5, 0.8),  # x coordinate
                np.random.normal(2, 0.4),     # y coordinate (reduced spread)
                0
            ])
            for _ in range(30)
        ]
        
        orange_final_positions = [
            np.array([
                np.random.normal(0.5, 0.8),   # x coordinate
                np.random.normal(2.5, 0.4),   # y coordinate (reduced spread)
                0
            ])
            for _ in range(30)
        ]

        # Move dots to their 2D positions
        self.play(
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.blue_dots, blue_final_positions)
            ],
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.orange_dots, orange_final_positions)
            ],
            run_time=2
        )
        self.wait(2) 