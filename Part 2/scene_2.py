from manim import *
import matplotlib.pyplot as plt
from manim_voiceover import VoiceoverScene
import numpy as np


class Scene2_2(VoiceoverScene, ThreeDScene):
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

        # CNN

        layer1 = self.create_cnn_layer().scale_to_fit_width(1)
        layer2 = (
            self.create_cnn_layer()
            .scale_to_fit_width(1)
            .next_to(layer1, RIGHT, buff=2.0)
        )
        layer3 = (
            self.create_cnn_layer()
            .scale_to_fit_width(1)
            .next_to(layer2, RIGHT, buff=2.0)
        )

        brace1 = Brace(layer1, DOWN, buff=0.1)
        txt = brace1.get_text("k = 3, s = 1").scale(0.5)
        brace1 = VGroup(brace1, txt)

        brace2 = Brace(layer2, DOWN, buff=0.1)
        txt2 = brace2.get_text("k = 5, s = 1").scale(0.5)
        brace2 = VGroup(brace2, txt2)

        brace3 = Brace(layer3, DOWN, buff=0.1)
        txt3 = brace3.get_text("k = 5, s = 2").scale(0.5)
        brace3 = VGroup(brace3, txt3)

        arrow1 = Arrow(layer1.get_right(), layer2.get_left(), stroke_width=2, buff=0.3)
        arrow2 = Arrow(layer2.get_right(), layer3.get_left(), stroke_width=2, buff=0.3)

        cnn = VGroup(layer1, brace1, layer2, brace2, layer3, brace3, arrow1, arrow2)
        cnn.move_to(ORIGIN)

        self.play(
            LaggedStart(
                FadeIn(layer1, brace1),
                GrowArrow(arrow1),
                FadeIn(layer2, brace2),
                GrowArrow(arrow2),
                FadeIn(layer3, brace3),
                lag_ratio=0.2,
            ),
            run_time=4,
        )

        self.wait(2)

        self.play(
            LaggedStart(
                ShowPassingFlash(Underline(txt), time_width=0.5),
                ShowPassingFlash(Underline(txt2), time_width=0.5),
                ShowPassingFlash(Underline(txt3), time_width=0.5),
                lag_ratio=0.5,
            ),
            run_time=2,
        )

        self.wait(0.5)

        self.play(FadeOut(cnn), run_time=1)

        formula = MathTex(
            r"r_0 = \sum_{l = 1}^{L} \left(  (k_l - 1) \prod_{i=1}^{l-1} s_i \right) + 1"
        ).scale(1.5)

        self.play(Write(formula), run_time=2)

        self.play(FadeOut(formula), run_time=0.7)

        # 1D Conv example

        example_layer = self.create_layer(9)
        example_kernel = self.create_kernel(3, RED).move_to(example_layer[4])

        self.play(FadeIn(example_layer), run_time=2)
        self.play(Create(example_kernel), run_time=1)

        self.play(example_kernel.animate.shift(0.5 * UP), run_time=1.0)
        self.play(example_kernel.animate.shift(0.5 * UP), run_time=1.0)
        self.play(example_kernel.animate.shift(0.5 * DOWN), run_time=1.0)
        self.play(example_kernel.animate.shift(0.5 * DOWN), run_time=1.0)
        self.play(FadeOut(example_layer), FadeOut(example_kernel), run_time=2)

        self.wait(2)


# Render the scene
if __name__ == "__main__":

    scene = Scene2_2()
    scene.render()
