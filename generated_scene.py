from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class GenScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang='en', tld='com'))

        main_content = VGroup()

        # Initial Binary Tree Node
        root_node = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)
        root_label = Text("Root", font_size=24, color=WHITE).move_to(root_node.get_center())
        main_content.add(root_node, root_label)

        # Left and Right Children
        left_node = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)
        right_node = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)

        left_label = Text("Left", font_size=24, color=WHITE).move_to(left_node.get_center())
        right_label = Text("Right", font_size=24, color=WHITE).move_to(right_node.get_center())

        left_node.next_to(root_node, DOWN + LEFT * 2, buff=1)
        left_label.move_to(left_node.get_center())
        right_node.next_to(root_node, DOWN + RIGHT * 2, buff=1)
        right_label.move_to(right_node.get_center())

        left_edge = Line(root_node.get_bottom(), left_node.get_top(), color=WHITE)
        right_edge = Line(root_node.get_bottom(), right_node.get_top(), color=WHITE)

        main_content.add(left_node, right_node, left_label, right_label, left_edge, right_edge)
        main_content.move_to(ORIGIN).shift(UP * 1)

        caption = Text("", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)
        self.add(caption)

        self.play(Create(root_node), Write(root_label))
        self.play(Write(caption, text="Creating the root node of the binary tree"))
        self.wait(2)

        with self.voiceover(text="Now, we add the left and right children to the root.") as tracker:
            self.play(
                Create(left_node), Create(right_node),
                Create(left_edge), Create(right_edge),
                Write(left_label), Write(right_label),
                Transform(caption, Text("Adding left and right children", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)),
                run_time=tracker.duration
            )
        self.wait(3)

        # Adding more nodes to the left subtree
        left_left_node = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)
        left_left_label = Text("Left-Left", font_size=24, color=WHITE).move_to(left_left_node.get_center())
        left_left_node.next_to(left_node, DOWN + LEFT * 2, buff=1)
        left_left_label.move_to(left_left_node.get_center())
        left_left_edge = Line(left_node.get_bottom(), left_left_node.get_top(), color=WHITE)

        left_right_node = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)
        left_right_label = Text("Left-Right", font_size=24, color=WHITE).move_to(left_right_node.get_center())
        left_right_node.next_to(left_node, DOWN + RIGHT * 2, buff=1)
        left_right_label.move_to(left_right_node.get_center())
        left_right_edge = Line(left_node.get_bottom(), left_right_node.get_top(), color=WHITE)

        main_content.add(left_left_node, left_right_node, left_left_label, left_right_label, left_left_edge, left_right_edge)

        with self.voiceover(text="Let's expand the left subtree by adding more nodes.") as tracker:
            self.play(
                Create(left_left_node), Create(left_right_node),
                Create(left_left_edge), Create(left_right_edge),
                Write(left_left_label), Write(left_right_label),
                Transform(caption, Text("Expanding the left subtree", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)),
                run_time=tracker.duration
            )
        self.wait(3)

        # Adding more nodes to the right subtree
        right_left_node = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)
        right_left_label = Text("Right-Left", font_size=24, color=WHITE).move_to(right_left_node.get_center())
        right_left_node.next_to(right_node, DOWN + LEFT * 2, buff=1)
        right_left_label.move_to(right_left_node.get_center())
        right_left_edge = Line(right_node.get_bottom(), right_left_node.get_top(), color=WHITE)

        right_right_node = Circle(radius=0.5, color=BLUE, fill_opacity=0.5)
        right_right_label = Text("Right-Right", font_size=24, color=WHITE).move_to(right_right_node.get_center())
        right_right_node.next_to(right_node, DOWN + RIGHT * 2, buff=1)
        right_right_label.move_to(right_right_node.get_center())
        right_right_edge = Line(right_node.get_bottom(), right_right_node.get_top(), color=WHITE)
        main_content.add(right_left_node, right_right_node, right_left_label, right_right_label, right_left_edge, right_right_edge)

        with self.voiceover(text="Similarly, let's add nodes to the right subtree.") as tracker:
            self.play(
                Create(right_left_node), Create(right_right_node),
                Create(right_left_edge), Create(right_right_edge),
                Write(right_left_label), Write(right_right_label),
                Transform(caption, Text("Expanding the right subtree", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)),
                run_time=tracker.duration
            )
        self.wait(3)
        
        # Highlighting a path
        path_nodes = [root_node, right_node, right_right_node]
        path_edges = [right_edge, right_right_edge]

        with self.voiceover(text="Now let's highlight a path from the root to a leaf node to demonstrate how we might traverse a binary tree.") as tracker:
            self.play(*[obj.animate.set_color(YELLOW) for obj in path_nodes + path_edges], Transform(caption, Text("Highlighting a path in the tree", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)), run_time=tracker.duration)
        self.wait(3)

        with self.voiceover(text="This visualization demonstrates the basic structure and construction of a binary tree. They are very helpful in organizing data.") as tracker:
            self.play(*[obj.animate.set_color(BLUE) for obj in path_nodes + path_edges],Transform(caption, Text("Binary trees are a fundamental data structure.", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)), run_time=tracker.duration)
        self.wait(3)

        # Explain the properties of Binary Tree
        binary_tree_properties = [
            "Each node has at most two children.",
            "Used in search algorithms and data storage.",
            "Can be traversed in various orders (in-order, pre-order, post-order)."
        ]

        properties_text = VGroup(*[Text(prop, font_size=24, color=WHITE).scale_to_fit_width(config.frame_width - 2) for prop in binary_tree_properties]).arrange(DOWN, center=True).to_edge(RIGHT, buff=0.5)
        properties_text.set_z_index(10)

        with self.voiceover(text="Let's quickly review the key properties of a binary tree.") as tracker:
            self.play(Write(properties_text),Transform(caption, Text("Key properties of a binary tree", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)), run_time=tracker.duration)
        self.wait(5)
        
        with self.voiceover(text="This concludes our exploration of binary trees. They are a fundamental concept in computer science.  Thanks for watching!") as tracker:
            self.play(FadeOut(main_content), FadeOut(properties_text), Transform(caption, Text("Thanks for watching!", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)), run_time=tracker.duration)
        self.wait(2)