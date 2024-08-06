from manim import *
import matplotlib.pyplot as plt
from manim_voiceover import VoiceoverScene
import numpy as np


class Scene2_3(VoiceoverScene, ThreeDScene):
    def create_layer(self, size):
        layer = VGroup()
        for _ in range(size):
            rect = Rectangle(height=0.5, width=0.5, stroke_width=1, stroke_color=WHITE)
            layer.add(rect)

        layer.arrange(DOWN, buff=0)

        return layer

    def create_kernel(self, size, color):
        kernel = VGroup()
        for _ in range(size):
            rect = Rectangle(
                height=0.5,
                width=0.5,
                stroke_width=2,
                stroke_color=color,
                fill_color=color,
                fill_opacity=0.2,
            )
            kernel.add(rect)

        kernel.arrange(DOWN, buff=0)

        return kernel

    def create_cnn_layer(self):

        f1 = Rectangle(
            height=1,
            width=1,
            fill_color=random_bright_color(),
            fill_opacity=1,
            stroke_width=0,
        )
        f2 = Rectangle(
            height=1,
            width=1,
            fill_color=random_bright_color(),
            fill_opacity=1,
            stroke_width=0,
        )
        f3 = Rectangle(
            height=1,
            width=1,
            fill_color=random_bright_color(),
            fill_opacity=1,
            stroke_width=0,
        )

        f2.shift(0.1 * f1.width * LEFT + 0.1 * f1.height * DOWN)
        f3.shift(0.2 * f1.width * LEFT + 0.2 * f1.height * DOWN)

        layer = VGroup(f1, f2, f3)

        return layer

    def construct(self):

        self.wait(2)

        # 1D Conv setup

        input_layer = self.create_layer(9)
        layer1 = self.create_layer(9).next_to(input_layer, RIGHT, buff=2.5)
        layer2 = self.create_layer(9).next_to(layer1, RIGHT, buff=2.5)

        layers = VGroup(input_layer, layer1, layer2).move_to(ORIGIN + 0.5 * UP)

        input_txt = Tex("f0").next_to(input_layer, UP, buff=0.5)
        layer1_txt = Tex("f1").next_to(layer1, UP, buff=0.5)
        layer2_txt = Tex("f2").next_to(layer2, UP, buff=0.5)

        self.play(FadeIn(input_layer), Write(input_txt), run_time=2)

        self.play(ShowPassingFlash(Underline(input_txt)), run_time=1)

        self.play(FadeIn(layer1), Write(layer1_txt), run_time=1)

        self.play(FadeIn(layer2), Write(layer2_txt), run_time=1)

        self.play(ShowPassingFlash(Underline(layer1_txt), time_width=0.5), run_time=1)

        self.play(ShowPassingFlash(Underline(layer2_txt), time_width=0.5), run_time=1)

        window1 = self.create_kernel(3, RED).move_to(input_layer[5])
        pixel1 = Rectangle(
            height=0.5, width=0.5, stroke_width=0.1, fill_color=RED, fill_opacity=1.0
        ).move_to(layer1[5])

        def get_lines_between_corners(k1, k2, color):
            corners1 = k1.get_corner(UR), k1.get_corner(DR)
            corners2 = k2.get_corner(UL), k2.get_corner(DL)
            lines = VGroup(
                *[
                    Line(c1, c2, color=color, stroke_width=2)
                    for c1, c2 in zip(corners1, corners2)
                ]
            )
            return lines

        # Create the pixel + window for the second layer

        pixel2 = Rectangle(
            height=0.5, width=0.5, stroke_width=0.1, fill_color=BLUE, fill_opacity=1.0
        ).move_to(layer2[4])
        window2 = self.create_kernel(3, BLUE).move_to(layer1[4])

        self.play(Create(pixel2), run_time=1)

        lines2 = always_redraw(lambda: get_lines_between_corners(window2, pixel2, BLUE))

        brace_k2 = Brace(window2, LEFT, buff=0.2)
        brace_k2_txt = brace_k2.get_text("k2").scale(0.5)

        self.play(Create(brace_k2), Write(brace_k2_txt), run_time=1)

        self.play(Create(window2), Create(lines2), run_time=1)

        # Create the pixel + window for the first layer

        self.play(Create(pixel1), run_time=1)

        self.play(FadeOut(brace_k2), FadeOut(brace_k2_txt), run_time=1)

        lines1 = always_redraw(lambda: get_lines_between_corners(window1, pixel1, RED))

        self.play(Create(window1), Create(lines1), run_time=1)

        brace_k1 = Brace(window1, LEFT, buff=0.2)
        brace_k1_txt = brace_k1.get_text("k1").scale(0.5)

        self.play(Create(brace_k1), Write(brace_k1_txt), run_time=1)

        self.wait(1)

        self.play(FadeOut(brace_k1), FadeOut(brace_k1_txt), run_time=1)

        # Move the window around

        self.play(
            pixel1.animate.shift(0.5 * UP),
            window1.animate.shift(0.5 * UP),
            run_time=1,
        )

        self.play(
            pixel1.animate.shift(0.5 * UP),
            window1.animate.shift(0.5 * UP),
            run_time=1,
        )

        self.play(pixel1.animate.shift(DOWN), window1.animate.shift(DOWN), run_time=1)

        self.wait(0.5)

        # Receptive field definition

        txt = (
            Tex("Number of features in a layer needed to compute one final feature")
            .to_edge(DOWN, buff=1.0)
            .scale(0.8)
        )

        self.play(Write(txt), run_time=2)

        self.wait(2)

        self.play(ApplyWave(txt), run_time=3)

        self.wait(0.5)

        self.play(FadeOut(window1, pixel1, lines1), run_time=1)

        # Show receptive field of layer 2 and write it

        self.play(FadeOut(txt), run_time=1)

        self.play(Create(brace_k2), Write(brace_k2_txt), run_time=1)

        self.wait(2)

        self.play(Indicate(window2, color=BLUE, scale_factor=1.2), run_time=1)

        self.wait(1)

        self.play(Indicate(pixel2, color=BLUE, scale_factor=1.2), run_time=1)

        txt = Tex("r2 = k2").to_edge(DOWN, buff=1.0)

        self.play(Write(txt), run_time=2)

        self.wait(1)

        txt_target = Tex("r2 = 3").to_edge(DOWN, buff=1.0)

        self.play(Transform(txt, txt_target), run_time=1)

        self.play(FadeOut(brace_k2, brace_k2_txt), run_time=1)

        self.play(FadeOut(txt), run_time=1)

        # Compute receptive field of layer 1

        formula = MathTex(r"r_1 = s_2 \times r_2 + (k_2 - s_2)").to_edge(DOWN, buff=1.0)
        formula_original = formula.copy()

        self.play(Write(formula), run_time=1)

        formula_target1 = MathTex(r"r_1 = 1 \times 3 + (3 - 1)").to_edge(DOWN, buff=1.0)
        formula_target2 = MathTex(r"r_1 = 3 + 2").to_edge(DOWN, buff=1.0)
        formula_target3 = MathTex(r"r_1 = 5").to_edge(DOWN, buff=1.0)

        self.play(Transform(formula, formula_target1), run_time=1)

        self.wait(0.5)

        self.play(Transform(formula, formula_target2), run_time=1)

        self.wait(0.5)

        self.play(Transform(formula, formula_target3), run_time=1)

        self.wait(0.5)

        self.play(Create(pixel1), run_time=1)

        self.play(Create(window1), Create(lines1), run_time=1)

        self.play(
            pixel1.animate.shift(0.5 * UP),
            window1.animate.shift(0.5 * UP),
            run_time=1,
        )

        self.play(
            pixel1.animate.shift(0.5 * UP),
            window1.animate.shift(0.5 * UP),
            run_time=1,
        )

        window1_target = self.create_kernel(5, RED).move_to(input_layer[4])
        pixel1_original = pixel1.copy().shift(DOWN)
        window1_original = window1.copy().shift(1.5 * DOWN)

        # Display the total area

        self.play(
            Transform(window1, window1_target),
            Transform(pixel1, window2.copy()),
            run_time=1,
        )

        brace_r1 = Brace(window1, LEFT, buff=0.2)
        brace_r1_txt = brace_r1.get_text("5").scale(0.5)

        self.play(Create(brace_r1), Write(brace_r1_txt), run_time=1)

        formula_target1 = MathTex(r"r_1 = 2 \times 3 + (3 - 2)").to_edge(DOWN, buff=1.0)
        formula_target2 = MathTex(r"r_1 = 6 + 1").to_edge(DOWN, buff=1.0)
        formula_target3 = MathTex(r"r_1 = 7").to_edge(DOWN, buff=1.0)

        self.play(Transform(formula, formula_target1), run_time=1)

        self.wait(0.5)

        self.play(Transform(formula, formula_target2), run_time=1)

        self.wait(0.5)

        self.play(Transform(formula, formula_target3), run_time=1)

        self.wait(0.5)

        # Now with a stride of 2

        self.play(
            Transform(window1, window1_original),
            Transform(pixel1, pixel1_original),
            FadeOut(brace_r1, brace_r1_txt),
            run_time=1,
        )

        self.play(
            pixel1.animate.shift(0.5 * UP),
            window1.animate.shift(1 * UP),
            run_time=1,
        )

        self.play(
            pixel1.animate.shift(0.5 * UP),
            window1.animate.shift(1 * UP),
            run_time=1,
        )

        # Display the total area

        window1_target = self.create_kernel(7, RED).move_to(input_layer[4])

        self.play(
            Transform(window1, window1_target),
            Transform(pixel1, window2.copy()),
            run_time=1,
        )

        brace_r1 = Brace(window1, LEFT, buff=0.2)
        brace_r1_txt = brace_r1.get_text("7").scale(0.5)

        self.play(Create(brace_r1), Write(brace_r1_txt), run_time=1)

        self.play(
            FadeOut(
                layers,
                input_txt,
                layer1_txt,
                layer2_txt,
                window1,
                pixel1,
                lines1,
                window2,
                pixel2,
                lines2,
                brace_r1,
                brace_r1_txt,
            ),
            run_time=1,
        )

        formula_original.move_to(ORIGIN).scale(1.5)

        self.play(Transform(formula, formula_original), run_time=1)

        self.wait(0.5)

        formula_target1 = MathTex(r"r_{l-1} = s_l \times r_l - (s_l - 1)").scale(1.5)

        self.play(Transform(formula, formula_target1), run_time=1)

        self.wait(0.5)

        formula_target = MathTex(
            r"r_0 = \sum_{l = 1}^{L} \left(  (k_l - 1) \prod_{i=1}^{l-1} s_i \right) + 1"
        ).scale(1.5)

        self.play(Transform(formula, formula_target), run_time=2)

        self.wait(0.5)

        self.play(FadeOut(formula), run_time=2)

        self.wait(2)


# Render the scene
if __name__ == "__main__":

    scene = Scene2_3()
    scene.render()
