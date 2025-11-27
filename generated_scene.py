from manim import *

class GenScene(Scene):
    def construct(self):
        # Define some objects
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 5, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": True, "numbers_to_exclude": [0]},
        )
        labels = axes.get_axis_labels(x_label="r", y_label="I(r)")

        # Define a function for moment of inertia (example: I = mr^2)
        def func(x):
            return x**2

        graph = axes.plot(func, x_range=[0, 3], color=BLUE)

        # Create a label for the graph
        graph_label = MathTex("I(r) = mr^2", color=BLUE)
        graph_label.next_to(graph, UP, buff=0.1)

        # Create a rotating object (circle) to represent mass rotating
        circle = Circle(radius=1, color=GREEN, fill_opacity=0.5).shift(DOWN*2+LEFT*4)
        dot = Dot(color=RED).move_to(circle.get_center())

        def update_circle(obj, dt):
            obj.rotate(dt*PI/2, about_point=dot.get_center()) # Rotate slowly
            return obj

        circle.add_updater(update_circle)

        # Show the objects on the screen
        self.play(Create(axes), Create(labels), run_time=2)
        self.play(Create(graph), Write(graph_label), run_time=3)
        self.play(Create(circle), Create(dot), run_time=2)
        self.wait(3)
        self.play(FadeOut(circle), FadeOut(dot), FadeOut(axes), FadeOut(labels), FadeOut(graph), FadeOut(graph_label), run_time=2)

        # Explain the concept with text
        text1 = Text("Moment of Inertia:", font_size=36)
        text2 = Text("Resistance to rotational acceleration.", font_size=24)
        text3 = Text("Depends on mass and its distribution relative to the axis of rotation.", font_size=24)

        text1.to_edge(UP)
        text2.next_to(text1, DOWN)
        text3.next_to(text2, DOWN)

        self.play(Write(text1), run_time=1)
        self.play(Write(text2), run_time=2)
        self.play(Write(text3), run_time=2)
        self.wait(3)
        self.play(FadeOut(text1), FadeOut(text2), FadeOut(text3), run_time=1)

        # Show the formula
        formula = MathTex("I = \\sum_i m_i r_i^2", font_size=48)
        formula.move_to(ORIGIN)
        self.play(Write(formula), run_time=2)

        text4 = Text("I: Moment of Inertia", font_size=24)
        text5 = Text("m: Mass", font_size=24)
        text6 = Text("r: Distance from axis of rotation", font_size=24)

        text4.next_to(formula, DOWN)
        text5.next_to(text4, DOWN)
        text6.next_to(text5, DOWN)

        self.play(Write(text4), run_time=1)
        self.play(Write(text5), run_time=1)
        self.play(Write(text6), run_time=1)

        self.wait(3)
        self.play(FadeOut(formula), FadeOut(text4), FadeOut(text5), FadeOut(text6), run_time=1)