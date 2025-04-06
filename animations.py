from manim import *
import numpy as np
from sklearn.svm import SVC

class BaseScene(Scene):
    def setup(self):
        super().setup()
        # Set white background
        self.camera.background_color = WHITE
        
        
        
        # Create the axes
        self.axes = Axes(
            x_range=[0, 8, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=6,
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
        self.x_label = Text("Weight", font_size=24, color=BLACK).next_to(self.axes.x_axis, DOWN*0.01)
        self.y_label = Text("Tail Length", font_size=24, color=BLACK).next_to(self.axes.y_axis, LEFT)
        
        # Group everything together
        self.axes_group = VGroup(self.axes, self.x_label, self.y_label)
        
        # Set random seed for reproducibility
        np.random.seed(273)
        
        # Generate coordinates for dots
        self.xy_coordinates_brown = [(np.random.normal(3.2, 1.5), np.random.normal(2, 1)) for _ in range(30)]
        self.xy_coordinates_orange = [(np.random.normal(5, 1.5), np.random.normal(4, 1)) for _ in range(30)]
        # print(self.xy_coordinates_orange)
        
        # Create initial positions (above x-axis)
        self.initial_positions_brown = [
            self.axes.c2p(
                np.random.normal(2, 0.5),  # x between 0 and 8
                np.random.normal(3, 0.5)   # y between 0.5 and 4 (above x-axis)
            )
            for _ in range(30)
        ]
        
        self.initial_positions_orange = [
            self.axes.c2p(
                np.random.normal(6, 0.5),  # x between 0 and 8
                np.random.normal(3, 0.5)   # y between 0.5 and 2 (above x-axis)
            )
            for _ in range(30)
        ]

        # Create dots using stored positions
        self.initial_brown_dots = VGroup(*[
            Dot(color="#562C0C").move_to(pos)            
            for pos in self.initial_positions_brown
        ])

        self.initial_orange_dots = VGroup(*[
            Dot(color="#FFA500").move_to(pos)
            for pos in self.initial_positions_orange
        ])

        # Create x-axis positions
        self.x_positions_brown = [self.axes.c2p(xy[0], 0) for xy in self.xy_coordinates_brown]
        self.x_positions_orange = [self.axes.c2p(xy[0], 0) for xy in self.xy_coordinates_orange]

        self.x_brown_dots = VGroup(*[
            Dot(color="#562C0C").move_to(pos)
            for pos in self.x_positions_brown
        ])

        self.x_orange_dots = VGroup(*[
            Dot(color="#FFA500").move_to(pos)
            for pos in self.x_positions_orange
        ])

        # Create 2D positions
        self.xy_positions_brown = [self.axes.c2p(xy[0], xy[1]) for xy in self.xy_coordinates_brown]
        self.xy_positions_orange = [self.axes.c2p(xy[0], xy[1]) for xy in self.xy_coordinates_orange]

        self.xy_brown_dots = VGroup(*[
            Dot(color="#562C0C").move_to(pos)
            for pos in self.xy_positions_brown
        ])

        self.xy_orange_dots = VGroup(*[
            Dot(color="#FFA500").move_to(pos)
            for pos in self.xy_positions_orange
        ])

class RandomDots(BaseScene):
    def construct(self):
        self.play(Create(self.initial_brown_dots), Create(self.initial_orange_dots))
        self.wait(2)

class ShowXAxis(BaseScene):
    def construct(self):
        self.add(self.initial_brown_dots, self.initial_orange_dots)
        self.wait()
        
        self.play(
            Create(self.axes.x_axis),
            Create(self.x_label)
        )
        self.wait(2)

class MoveDots1D(BaseScene):
    def construct(self):
        self.add(self.initial_brown_dots, self.initial_orange_dots, self.axes.x_axis, self.x_label)
        self.wait()

        self.play(
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.initial_brown_dots, self.x_positions_brown)
            ],
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.initial_orange_dots, self.x_positions_orange)
            ],
            run_time=2
        )
        self.wait(2)

class ShowBrackets(BaseScene):
    def construct(self):
        self.add(self.x_brown_dots, self.x_orange_dots, self.axes.x_axis, self.x_label)
        
        # Create left bracket (0-4)
        left_bracket = BraceBetweenPoints(
            self.axes.c2p(0, 1),  # Start point
            self.axes.c2p(4, 1),  # End point
            direction=UP,
            color="#562C0C"
        )
        
        # Create right bracket (4-8)
        right_bracket = BraceBetweenPoints(
            self.axes.c2p(4, 1),  # Start point
            self.axes.c2p(8, 1),  # End point
            direction=UP,
            color="#F5A739"
        )
        
        # Show brackets
        self.play(
            Create(left_bracket),
            Create(right_bracket)
        )
        self.wait(2)

class AnimateBrackets(BaseScene):
    def construct(self):
        self.add(self.x_brown_dots, self.x_orange_dots, self.axes.x_axis, self.x_label)
        
        def get_brackets(t):
            # Calculate intersection point using sine wave
            intersection = 4 + 3 * np.sin((2 * PI) * 1.02 * t)
            
            # Create brackets
            left_bracket = BraceBetweenPoints(
                self.axes.c2p(0, 1),
                self.axes.c2p(intersection, 1),
                direction=UP,
                color="#562C0C"
            )
            right_bracket = BraceBetweenPoints(
                self.axes.c2p(intersection, 1),
                self.axes.c2p(8, 1),
                direction=UP,
                color="#F5A739"
            )
            return VGroup(left_bracket, right_bracket)
        
        # Create initial brackets
        brackets = get_brackets(0)
        
        # Create the animation
        self.play(
            UpdateFromAlphaFunc(
                brackets,
                lambda m, t: m.become(get_brackets(t))
            ),
            run_time=4,
            rate_func=linear
        )
        self.wait(2)

class ShowYAxis(BaseScene):
    def construct(self):
        self.add(self.x_brown_dots, self.x_orange_dots, self.axes.x_axis, self.x_label)
        
        self.play(
            Create(self.axes.y_axis),
            Create(self.y_label)
        )
        self.wait(2)

class MoveDots2D(BaseScene):
    def construct(self):
        self.add(self.x_brown_dots, self.x_orange_dots, self.axes_group)
        
        self.play(
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.x_brown_dots, self.xy_positions_brown)
            ],
            *[
                dot.animate.move_to(pos)
                for dot, pos in zip(self.x_orange_dots, self.xy_positions_orange)
            ],
            run_time=2
        )
        self.wait(2)

class ShowModel2D(BaseScene):
    def construct(self):
        self.add(self.xy_brown_dots, self.xy_orange_dots, self.axes_group)
        
        # Extract coordinates from dot positions
        brown_coords = np.array([self.axes.p2c(dot.get_center()) for dot in self.xy_brown_dots])
        orange_coords = np.array([self.axes.p2c(dot.get_center()) for dot in self.xy_orange_dots])
        
        # Prepare data for SVM
        X = np.vstack([brown_coords, orange_coords])
        y = np.array([0] * len(brown_coords) + [1] * len(orange_coords))
        
        # Train SVM
        clf = SVC(kernel='linear')
        clf.fit(X, y)
        
        # Get the decision boundary parameters
        w = clf.coef_[0]
        b = clf.intercept_[0]
        
        # Calculate line endpoints (at the edges of the plot)
        x_min, x_max = 0, 8
        y_min, y_max = 0, 6
        
        # Calculate y values for the line at x_min and x_max
        y1 = (-w[0] * x_min - b) / w[1]
        y2 = (-w[0] * x_max - b) / w[1]
        
        # Clip y values to plot boundaries
        y1 = np.clip(y1, y_min, y_max)
        y2 = np.clip(y2, y_min, y_max)
        
        # Create the decision boundary line
        decision_line = Line(
            start=self.axes.c2p(x_min, y1),
            end=self.axes.c2p(x_max, y2),
            color=BLACK,
            stroke_width=2
        )
        
        # Create colored regions
        # Left region (brown)
        left_region = Polygon(
            self.axes.c2p(x_min, y_min),
            self.axes.c2p(x_min, y1),
            self.axes.c2p(x_max, y2),
            self.axes.c2p(x_max, y_min),
            color="#562C0C",
            fill_opacity=0.3,
            stroke_width=0
        )
        
        # Right region (orange)
        right_region = Polygon(
            self.axes.c2p(x_min, y1),
            self.axes.c2p(x_min, y_max),
            self.axes.c2p(x_max, y_max),
            self.axes.c2p(x_max, y2),
            color="#F5A739",
            fill_opacity=0.3,
            stroke_width=0
        )
        
        # Show the decision boundary and regions
        self.play(
            Create(decision_line),
            FadeIn(left_region),
            FadeIn(right_region)
        )
        self.wait(2)
        

class Show3DPlot(ThreeDScene):
    def construct(self):
        # Set white background
        self.camera.background_color = WHITE
        
        # Set orthographic projection (no perspective)
        self.camera.projection_matrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1]
        ])
        
        # Set random seed for reproducibility
        np.random.seed(42)
        
        # Create 3D axes
        axes = ThreeDAxes(
            x_range=[0, 8, 1],  # Weight (same as 2D)
            y_range=[0, 8, 1],  # Height (new dimension)
            z_range=[0, 6, 1],  # Tail Length (was y in 2D)
            x_length=8,
            y_length=6,
            z_length=6,
        )
        
        # Add labels
        x_label = Text("Weight", font_size=24, color=BLACK).next_to(axes.x_axis, IN).rotate(PI/2, axis=RIGHT)
        y_label = Text("Height", font_size=24, color=BLACK).next_to(axes.y_axis, LEFT)
        z_label = Text("Tail Length", font_size=24, color=BLACK).next_to(axes.z_axis, LEFT).rotate(-PI/2, axis=LEFT)

        # Set random seed for reproducibility
        np.random.seed(273)
        
        # Generate coordinates for dots
        self.xy_coordinates_brown = [(np.random.normal(3.2, 1.5), np.random.normal(2, 1)) for _ in range(30)]
        self.xy_coordinates_orange = [(np.random.normal(5, 1.5), np.random.normal(4, 1)) for _ in range(30)]
        # print(self.xy_coordinates_orange)
        
        
        # Create 3D dots using existing XY positions and adding Y variation
        brown_dots = VGroup(*[
            Dot3D(
                point=axes.c2p(
                    pos[0],  # x from existing position (Weight)
                    np.random.normal(1, 0.4),  # y variation (Height)
                    pos[1],  # z from existing position (Tail Length)
                ),
                color="#562C0C",
                radius=0.05
            )
            for pos in self.xy_coordinates_brown
        ])
        
        orange_dots = VGroup(*[
            Dot3D(
                point=axes.c2p(
                    pos[0],  # x from existing position (Weight)
                    np.random.normal(3.5, 0.4),  # y variation (Height)
                    pos[1],  # z from existing position (Tail Length)
                ),
                color="#F5A739",
                radius=0.05
            )
            for pos in self.xy_coordinates_orange
        ])
        
        # Set initial camera orientation to match 2D view
        # Looking directly along the y-axis (height axis)
        self.set_camera_orientation(phi=90*DEGREES, theta=-90*DEGREES)
        self.camera.frame_center = axes.c2p(4, 0, 5.5)  # Offset camera position in data coordinates
        
        # Add all elements
        self.add(axes, x_label, y_label, z_label, brown_dots, orange_dots)
        
        # Wait to show 2D view
        self.wait(2)
        
        # Animate camera rotation to reveal 3D
        self.move_camera(
            phi=60*DEGREES,  # Tilt up to show height
            theta=-30*DEGREES,  # Rotate to show 3D perspective
            frame_center=axes.c2p(4, 3, 7),  # Maintain offset during rotation
            run_time=3
        )
        
        # Add y_label after rotation
        self.add(y_label)
        
        self.wait(2) 