from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class GenScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(lang='en', tld='com'))

        main_content = VGroup()
        main_content.move_to(ORIGIN).shift(UP * 1)
        
        # Initial array
        array = [5, 1, 4, 2, 8]
        rects = []
        texts = []
        
        for i, num in enumerate(array):
            rect = Rectangle(width=1, height=1, color=WHITE, fill_opacity=0.5)
            rect.move_to([i, 0, 0])
            text = Text(str(num), color=WHITE, font_size=32, stroke_width=2, stroke_color=BLACK)
            text.move_to(rect.get_center())
            rects.append(rect)
            texts.append(text)

        group = VGroup(*rects, *texts)
        group.arrange(RIGHT, buff=0)

        caption = Text("Bubble Sort Visualization", font_size=32, stroke_width=2, stroke_color=BLACK)
        caption.to_edge(DOWN, buff=0.5)
        self.add(caption)

        main_content.add(group)
        main_content.move_to(ORIGIN).shift(UP * 1)
        self.add(main_content)

        with self.voiceover(text="Let's visualize the bubble sort algorithm step by step.") as tracker:
            self.play(Create(group), run_time=tracker.duration)
            self.wait(1)

        swaps_made = True
        iteration = 0

        while swaps_made:
            swaps_made = False
            iteration += 1

            iteration_text = Text(f"Iteration: {iteration}", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)
            self.play(Transform(caption, iteration_text))

            for i in range(len(array) - 1):
                with self.voiceover(text=f"Comparing {array[i]} and {array[i+1]}.") as tracker:
                    self.play(
                        rects[i].animate.set_fill(YELLOW),
                        rects[i+1].animate.set_fill(YELLOW),
                        run_time=tracker.duration
                    )
                self.wait(0.5)

                if array[i] > array[i + 1]:
                    with self.voiceover(text=f"Swapping {array[i]} and {array[i+1]} because {array[i]} is greater than {array[i+1]}.") as tracker:
                        temp = array[i]
                        array[i] = array[i + 1]
                        array[i + 1] = temp
                        swaps_made = True

                        # Animate the swap
                        self.play(
                            rects[i].animate.move_to(rects[i+1].get_center()),
                            rects[i+1].animate.move_to(rects[i].get_center()),
                            texts[i].animate.move_to(rects[i+1].get_center()),
                            texts[i+1].animate.move_to(rects[i].get_center()),
                            run_time=tracker.duration
                        )

                        rects[i], rects[i+1] = rects[i+1], rects[i]
                        texts[i], texts[i+1] = texts[i+1], texts[i]

                        
                    self.wait(1)

                with self.voiceover(text="Comparison complete.") as tracker:
                    self.play(
                        rects[i].animate.set_fill(WHITE, opacity=0.5),
                        rects[i+1].animate.set_fill(WHITE, opacity=0.5),
                        run_time=tracker.duration
                    )
                self.wait(0.5)

        with self.voiceover(text="The array is now sorted.") as tracker:
            pass # Removed the problematic play statement
            
        sorted_text = Text("Sorted!", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)
        self.play(Transform(caption, sorted_text))
        self.wait(3)

        explanation_text = Text("Bubble Sort: Compares adjacent elements and swaps them if they are in the wrong order. Repeats until no swaps are needed.", font_size=32, stroke_width=2, stroke_color=BLACK).scale_to_fit_width(config.frame_width - 2)
        explanation_text.to_edge(DOWN, buff=0.5)
        
        with self.voiceover(text="Bubble sort is a simple sorting algorithm that repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order. The pass through the list is repeated until no swaps are needed, which indicates that the list is sorted.") as tracker:
            self.play(Transform(caption, explanation_text), run_time=tracker.duration)
        self.wait(5)

        complexity_text = Text("Time Complexity: O(n^2)", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)
        with self.voiceover(text="The time complexity of bubble sort is O of n squared, which means it is not efficient for large lists.") as tracker:
            self.play(Transform(caption, complexity_text), run_time=tracker.duration)
        self.wait(3)

        best_case_text = Text("Best Case Time Complexity: O(n)", font_size=32, stroke_width=2, stroke_color=BLACK).to_edge(DOWN, buff=0.5)
        with self.voiceover(text="In the best case, when the list is already sorted, the time complexity is O of n.") as tracker:
            self.play(Transform(caption, best_case_text), run_time=tracker.duration)
        self.wait(3)

        self.wait(2)