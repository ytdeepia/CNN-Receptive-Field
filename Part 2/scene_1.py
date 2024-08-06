from manim import *
import matplotlib.pyplot as plt
from manim_voiceover import VoiceoverScene
import numpy as np


class Scene2_1(VoiceoverScene, ThreeDScene):
    def create_layer(self):

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

    def create_img(self, img_path):
        img = (
            ImageMobject(img_path)
            .set_resampling_algorithm(RESAMPLING_ALGORITHMS["none"])
            .scale(15)
        )

        lattice = NumberPlane(
            x_range=[-14, 14],
            y_range=[-14, 14],
            x_length=2,
            y_length=2,
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "stroke_opacity": 1,
            },
            axis_config={
                "stroke_color": GRAY,
                "stroke_width": 1,
                "include_numbers": False,
            },
            faded_line_ratio=0,
        )

        lattice.scale_to_fit_width(img.width)
        lattice.move_to(img.get_center())
        input_img_rect = SurroundingRectangle(img, color=GRAY, stroke_width=1, buff=0)
        img = Group(img, lattice, input_img_rect)

        return img

    def construct(self):
        self.wait(2)

        # Image + lattice

        input_img = self.create_img("images/0_mnist.png")
        img_conv1 = self.create_img("images/mnist_conv1.png")
        img_conv2 = self.create_img("images/mnist_conv2.png")

        input_img.to_corner(UL)
        img_conv1.to_edge(UP)
        img_conv2.to_corner(UR)

        self.play(FadeIn(input_img))

        # CNN

        layer1 = self.create_layer().scale_to_fit_width(1)
        layer2 = (
            self.create_layer().scale_to_fit_width(1).next_to(layer1, RIGHT, buff=2.0)
        )
        layer3 = (
            self.create_layer().scale_to_fit_width(1).next_to(layer2, RIGHT, buff=2.0)
        )

        brace1 = Brace(layer1, DOWN, buff=0.1)
        txt = brace1.get_text("3 x 3").scale(0.5)
        brace1 = VGroup(brace1, txt)

        brace2 = Brace(layer2, DOWN, buff=0.1)
        txt2 = brace2.get_text("3 x 3").scale(0.5)
        brace2 = VGroup(brace2, txt2)

        brace3 = Brace(layer3, DOWN, buff=0.1)
        txt3 = brace3.get_text("3 x 3").scale(0.5)
        brace3 = VGroup(brace3, txt3)

        arrow1 = Arrow(layer1.get_right(), layer2.get_left(), stroke_width=2, buff=0.3)
        arrow2 = Arrow(layer2.get_right(), layer3.get_left(), stroke_width=2, buff=0.3)

        cnn = VGroup(layer1, brace1, layer2, brace2, layer3, brace3, arrow1, arrow2)
        cnn.move_to(ORIGIN).to_edge(DOWN, buff=0.5)

        self.wait(2)

        self.play(
            LaggedStart(
                FadeIn(layer1, brace1),
                GrowArrow(arrow1),
                FadeIn(layer2, brace2),
                GrowArrow(arrow2),
                FadeIn(layer3, brace3),
                lag_ratio=0.2,
            ),
        )

        # Highlight first layer

        high_rect_layer1 = SurroundingRectangle(
            layer1, color=ORANGE, stroke_width=4, buff=0.2
        )

        self.play(ShowPassingFlash(high_rect_layer1, time_width=0.1), run_time=2)

        # Window input image

        cell_width = input_img.width / 56
        window_layer1 = Rectangle(
            height=3 * cell_width,
            width=3 * cell_width,
            color=ORANGE,
            fill_opacity=0,
            stroke_width=2,
        )
        window_layer1.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        self.play(Create(window_layer1), run_time=2)

        # Create feature map 1

        self.play(FadeIn(img_conv1), FadeOut(window_layer1), run_time=2)

        # Highlight second layer

        high_rect_layer2 = SurroundingRectangle(
            layer2, color=BLUE, stroke_width=4, buff=0.2
        )

        self.play(ShowPassingFlash(high_rect_layer2, time_width=0.1, run_time=2))

        # Window second layer

        window_layer2 = Rectangle(
            height=3 * cell_width,
            width=3 * cell_width,
            color=BLUE,
            fill_opacity=0,
            stroke_width=2,
        )
        window_layer2.move_to(
            img_conv1.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        self.play(Create(window_layer2), run_time=2)

        # Focus on one pixel

        pixel_layer2 = Rectangle(
            height=cell_width,
            width=cell_width,
            color=BLUE,
            fill_opacity=1.0,
            stroke_width=2,
        )
        pixel_layer2.move_to(window_layer2.get_center()).shift(
            cell_width * LEFT + cell_width * UP
        )

        def get_lines_between_corners(r1, r2, color):
            corners1 = (
                r1.get_corner(UL),
                r1.get_corner(UR),
                r1.get_corner(DL),
                r1.get_corner(DR),
            )
            corners2 = (
                r2.get_corner(UL),
                r2.get_corner(UR),
                r2.get_corner(DL),
                r2.get_corner(DR),
            )
            lines = VGroup(
                *[
                    Line(c1, c2, color=color, stroke_width=2)
                    for c1, c2 in zip(corners1, corners2)
                ]
            )
            return lines

        self.play(Create(pixel_layer2))

        # Window first layer

        window_layer1 = Rectangle(
            height=3 * cell_width,
            width=3 * cell_width,
            color=BLUE,
            fill_opacity=0.3,
            stroke_width=2,
        )
        window_layer1.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )
        window_layer1.shift(cell_width * LEFT + cell_width * UP)

        # Create initial lines
        lines = always_redraw(
            lambda: get_lines_between_corners(pixel_layer2, window_layer1, BLUE)
        )

        self.play(
            LaggedStart(Create(lines), Create(window_layer1), lag_ratio=0.3),
            run_time=1,
        )

        # Moving the pixel and the window

        pixel_and_window_layer1 = VGroup(pixel_layer2, window_layer1, lines)

        shifts = [
            cell_width * RIGHT,
            cell_width * RIGHT,
            cell_width * DOWN + 2 * cell_width * LEFT,
            cell_width * RIGHT,
            cell_width * RIGHT,
            cell_width * DOWN + 2 * cell_width * LEFT,
            cell_width * RIGHT,
            cell_width * RIGHT,
        ]

        for shift in shifts:
            self.play(pixel_and_window_layer1.animate.shift(shift), run_time=0.5)

        # Highlight bigger window layer 1

        window_layer1_target = Rectangle(
            height=5 * cell_width,
            width=5 * cell_width,
            color=BLUE,
            fill_opacity=0.3,
            stroke_width=2,
        )
        window_layer1_target.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )
        self.play(
            Transform(window_layer1, window_layer1_target),
            Transform(pixel_layer2, window_layer2.copy()),
            run_time=3,
        )

        # Fadeout first windows

        self.play(FadeOut(pixel_and_window_layer1, window_layer2), run_time=1)

        self.play(FadeIn(img_conv2), run_time=2)

        # Highlight third layer

        high_rect_layer3 = SurroundingRectangle(
            layer3, color=GREEN, stroke_width=4, buff=0.2
        )

        self.play(ShowPassingFlash(high_rect_layer3, time_width=0.1, run_time=2))

        # Window third layer

        window_layer3 = Rectangle(
            height=3 * cell_width,
            width=3 * cell_width,
            color=GREEN,
            fill_opacity=0,
            stroke_width=2,
        )
        window_layer3.move_to(
            img_conv2.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        self.play(Create(window_layer3), run_time=2)

        # Focus on one pixel

        pixel_layer3 = Rectangle(
            height=cell_width,
            width=cell_width,
            color=GREEN,
            fill_opacity=1.0,
            stroke_width=2,
        )
        pixel_layer3.move_to(window_layer3.get_center()).shift(
            cell_width * LEFT + cell_width * UP
        )

        self.play(Create(pixel_layer3), run_time=1)

        # Window second layer

        window_layer2 = Rectangle(
            height=3 * cell_width,
            width=3 * cell_width,
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=2,
        )
        window_layer2.move_to(
            img_conv1.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )
        window_layer2.shift(cell_width * LEFT + cell_width * UP)

        # Create initial lines between layer 3 and layer 2

        lines3 = always_redraw(
            lambda: get_lines_between_corners(pixel_layer3, window_layer2, GREEN)
        )

        self.play(
            LaggedStart(Create(lines3), Create(window_layer2), lag_ratio=0.3),
            run_time=1,
        )

        # Create initial lines between layer 2 and layer 1

        window_layer1 = Rectangle(
            height=5 * cell_width,
            width=5 * cell_width,
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=2,
        )
        window_layer1.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )
        window_layer1.shift(cell_width * LEFT + cell_width * UP)

        lines2 = always_redraw(
            lambda: get_lines_between_corners(window_layer2, window_layer1, GREEN)
        )

        self.wait(1)

        self.play(
            LaggedStart(Create(lines2), Create(window_layer1), lag_ratio=0.3),
            run_time=1,
        )

        # Move the pixel and the windows

        pixel_and_windows = VGroup(
            pixel_layer3, window_layer2, window_layer1, lines2, lines3
        )

        for shift in shifts:
            self.play(pixel_and_windows.animate.shift(shift), run_time=0.5)

        # Highlight bigger window layer 2

        window_layer2_target = Rectangle(
            height=5 * cell_width,
            width=5 * cell_width,
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=2,
        )
        window_layer2_target.move_to(
            img_conv1.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        window_layer1_target = Rectangle(
            height=7 * cell_width,
            width=7 * cell_width,
            color=GREEN,
            fill_opacity=0.3,
            stroke_width=2,
        )
        window_layer1_target.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        self.play(
            Transform(window_layer2, window_layer2_target),
            Transform(pixel_layer3, window_layer3.copy()),
            Transform(window_layer1, window_layer1_target),
            run_time=2,
        )

        # Fade out the windows
        self.play(FadeOut(pixel_and_windows, window_layer3), run_time=2)
        self.play(FadeOut(input_img, img_conv1, img_conv2, cnn, run_time=1))

        txt = Tex("The receptive field increases with the number of layers !")
        self.play(Write(txt), run_time=1)

        underline = Underline(txt, color=WHITE)

        self.play(ShowPassingFlash(underline, time_width=0.1), run_time=1)

        self.wait(2)


# Render the scene
if __name__ == "__main__":

    scene = Scene2_1()
    scene.render()
