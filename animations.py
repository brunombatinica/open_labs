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

    def get_decision_line(self, m, c): 
        # Calculate line endpoints (at the edges of the plot)
        x_min, x_max = 0, 8
        y_min, y_max = 0, 6
        
        # Calculate all possible intersection points
        # With vertical boundaries
        y_left = m * x_min + c   # y at x = x_min
        y_right = m * x_max + c  # y at x = x_max
        
        # With horizontal boundaries
        x_bottom = (y_min - c) / m if m != 0 else None  # x at y = y_min
        x_top = (y_max - c) / m if m != 0 else None     # x at y = y_max
        
        # Collect all valid intersection points
        points = []
        
        # Check intersections with vertical boundaries
        if y_min <= y_left <= y_max:
            points.append((x_min, y_left))
        if y_min <= y_right <= y_max:
            points.append((x_max, y_right))
            
        # Check intersections with horizontal boundaries
        if x_bottom is not None and x_min <= x_bottom <= x_max:
            points.append((x_bottom, y_min))
        if x_top is not None and x_min <= x_top <= x_max:
            points.append((x_top, y_max))
        
        # Sort points by x-coordinate to ensure correct line direction
        points.sort()
        
        # Take the first and last points to draw the line
        if len(points) >= 2:
            start_point = self.axes.c2p(*points[0])
            end_point = self.axes.c2p(*points[-1])
        else:
            # Fallback if no valid intersections (shouldn't happen with our setup)
            start_point = self.axes.c2p(x_min, y_min)
            end_point = self.axes.c2p(x_max, y_max)
        
        return Line(
            start=start_point,
            end=end_point,
            color=BLACK,
            stroke_width=2
        )
    
    def get_regions(self, m, c):
        # Calculate line endpoints (at the edges of the plot)
        x_min, x_max = 0, 8
        y_min, y_max = 0, 6
        
        # Calculate all possible intersection points
        # With vertical boundaries
        y_left = m * x_min + c   # y at x = x_min
        y_right = m * x_max + c  # y at x = x_max
        
        # With horizontal boundaries
        x_bottom = (y_min - c) / m if m != 0 else None  # x at y = y_min
        x_top = (y_max - c) / m if m != 0 else None     # x at y = y_max
        
        # Collect all valid intersection points
        points = []
        
        # Check intersections with vertical boundaries
        if y_min <= y_left <= y_max:
            points.append((x_min, y_left))
        if y_min <= y_right <= y_max:
            points.append((x_max, y_right))
            
        # Check intersections with horizontal boundaries
        if x_bottom is not None and x_min <= x_bottom <= x_max:
            points.append((x_bottom, y_min))
        if x_top is not None and x_min <= x_top <= x_max:
            points.append((x_top, y_max))
        
        # Sort points by x-coordinate to ensure correct line direction
        points.sort()
        
        # Create region vertices
        if len(points) >= 2:
            # Left region (brown)
            left_region = Polygon(
                self.axes.c2p(x_min, y_min),
                self.axes.c2p(x_min, min(y_max, points[0][1])),
                self.axes.c2p(*points[0]),
                self.axes.c2p(*points[-1]),
                self.axes.c2p(x_max, y_min),
                color="#562C0C",
                fill_opacity=0.3,
                stroke_width=0
            )
            
            # Right region (orange)
            right_region = Polygon(
                self.axes.c2p(*points[0]),
                self.axes.c2p(x_min, y_max),
                self.axes.c2p(x_max, y_max),
                self.axes.c2p(x_max, max(y_min, points[-1][1])),
                self.axes.c2p(*points[-1]),
                color="#F5A739",
                fill_opacity=0.3,
                stroke_width=0
            )
        else:
            # Fallback if no valid intersections (shouldn't happen with our setup)
            left_region = Polygon(
                self.axes.c2p(x_min, y_min),
                self.axes.c2p(x_min, y_max),
                self.axes.c2p(x_max, y_max),
                self.axes.c2p(x_max, y_min),
                color="#562C0C",
                fill_opacity=0.3,
                stroke_width=0
            )
            right_region = Polygon(
                self.axes.c2p(x_min, y_min),
                self.axes.c2p(x_min, y_max),
                self.axes.c2p(x_max, y_max),
                self.axes.c2p(x_max, y_min),
                color="#F5A739",
                fill_opacity=0.3,
                stroke_width=0
            )
        
        return VGroup(left_region, right_region)

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

class ShowInitialModel(BaseScene):
    def construct(self):
        self.add(self.xy_brown_dots, self.xy_orange_dots, self.axes_group)
        
        # Initial decision boundary: y = -x + 4
        m_initial = -(5/7)  # Slope
        c_initial = 5   # Intercept
        
        # Create initial decision boundary and regions
        initial_line = self.get_decision_line(m_initial, c_initial)
        initial_regions = self.get_regions(m_initial, c_initial)
        
        # Show initial decision boundary and regions
        self.play(
            Create(initial_line),
            FadeIn(initial_regions)
        )
        self.wait(2)

class OptimizeModel(BaseScene):
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
        
        # Convert SVC parameters to slope-intercept form (y = mx + c)
        # From w[0]*x + w[1]*y + b = 0
        # to y = (-w[0]/w[1])x + (-b/w[1])
        w = clf.coef_[0]
        b = clf.intercept_[0]
        m_optimal = -w[0]/w[1]  # Slope
        c_optimal = -b/w[1]     # Intercept
        
        # Initial decision boundary: y = -x + 4
        m_initial = -(5/7)  # Slope
        c_initial = 5   # Intercept
        
        # Create initial decision boundary and regions
        initial_line = self.get_decision_line(m_initial, c_initial)
        initial_regions = self.get_regions(m_initial, c_initial)
        
        # Add initial boundary and regions
        self.add(initial_line, initial_regions)
        self.wait(1)
        
        # Create animation for fluctuating decision boundary
        def get_fluctuating_boundary(t):
            # Oscillate between initial and optimal parameters
            if t < 0.8:
                # First 80%: fluctuate around initial parameters with gradual start
                # Start at -PI/5 and complete one full cycle
                m = m_initial - (1 + np.sin( (2 * PI * t / 0.8) * 3 - PI/2)) * 0.5
                c = c_initial + (1 - np.cos( (2 * PI * t / 0.8) * 2)) * 2
            else:
                # Last 20%: transition to optimal parameters
                progress = (t - 0.8) * 5  # Scale to 0-1 range
                m = m_initial + (m_optimal - m_initial) * progress
                c = c_initial + (c_optimal - c_initial) * progress
            
            return VGroup(
                self.get_decision_line(m, c),
                self.get_regions(m, c)
            )
        
        # Create the animation
        boundary_group = VGroup(initial_line, initial_regions)
        self.play(
            UpdateFromAlphaFunc(
                boundary_group,
                lambda m, t: m.become(get_fluctuating_boundary(t))
            ),
            run_time=6,
            rate_func=linear
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
        self.camera.frame_center = axes.c2p(4, 0, 4.5)  # Offset camera position in data coordinates
        
        # Add all elements
        self.add(axes, x_label, y_label, z_label, brown_dots, orange_dots)
        
        # Wait to show 2D view
        self.wait(2)
        
        # Animate camera rotation to reveal 3D
        self.move_camera(
            phi=60*DEGREES,  # Tilt up to show height
            theta=-30*DEGREES,  # Rotate to show 3D perspective
            frame_center=axes.c2p(4, 3, 5),  # Maintain offset during rotation
            run_time=3
        )
        
        # Add y_label after rotation
        self.add(y_label)
        
        self.wait(2) 