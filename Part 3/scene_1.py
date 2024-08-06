from manim import *
import matplotlib.pyplot as plt
from manim_voiceover import VoiceoverScene
import numpy as np


class Scene3_1(VoiceoverScene, ThreeDScene):
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

        # CNN

        layer1 = self.create_layer().scale_to_fit_width(1)
        layer2 = (
            self.create_layer().scale_to_fit_width(1).next_to(layer1, RIGHT, buff=2.0)
        )
        layer3 = (
            self.create_layer().scale_to_fit_width(1).next_to(layer2, RIGHT, buff=2.0)
        )
        layer4 = (
            self.create_layer().scale_to_fit_width(1).next_to(layer3, RIGHT, buff=2.0)
        )
        layer5 = (
            self.create_layer().scale_to_fit_width(1).next_to(layer4, RIGHT, buff=2.0)
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

        brace4 = Brace(layer4, DOWN, buff=0.1)
        txt4 = brace4.get_text("3 x 3").scale(0.5)
        brace4 = VGroup(brace4, txt4)

        brace5 = Brace(layer5, DOWN, buff=0.1)
        txt5 = brace5.get_text("3 x 3").scale(0.5)
        brace5 = VGroup(brace5, txt5)

        arrow1 = Arrow(layer1.get_right(), layer2.get_left(), stroke_width=2, buff=0.3)
        arrow2 = Arrow(layer2.get_right(), layer3.get_left(), stroke_width=2, buff=0.3)
        arrow3 = Arrow(layer3.get_right(), layer4.get_left(), stroke_width=2, buff=0.3)
        arrow4 = Arrow(layer4.get_right(), layer5.get_left(), stroke_width=2, buff=0.3)

        cnn = VGroup(
            layer1,
            brace1,
            layer2,
            brace2,
            layer3,
            brace3,
            layer4,
            brace4,
            layer5,
            brace5,
            arrow1,
            arrow2,
            arrow3,
            arrow4,
        )

        cnn.scale(0.9).move_to(ORIGIN).to_edge(DOWN, buff=0.5)

        self.play(
            LaggedStart(
                FadeIn(layer1, brace1),
                GrowArrow(arrow1),
                FadeIn(layer2, brace2),
                GrowArrow(arrow2),
                FadeIn(layer3, brace3),
                GrowArrow(arrow3),
                FadeIn(layer4, brace4),
                GrowArrow(arrow4),
                FadeIn(layer5, brace5),
                lag_ratio=0.2,
            ),
            run_time=2,
        )

        # Image

        input_img = self.create_img("images/0_mnist.png").scale(1.3)
        input_img.to_edge(UP, buff=1.0)

        self.play(FadeIn(input_img), run_time=2)

        # Theoretical receptive field

        trf_title = Tex("Theoretical Receptive Field", color=BLUE).scale(0.4)
        cell_width = input_img[0].width / 28

        trf = Rectangle(
            height=11 * cell_width,
            width=11 * cell_width,
            stroke_width=2,
            stroke_color=BLUE,
        )

        trf.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        trf_line = Line(
            start=trf.get_corner(UR),
            end=trf.get_corner(UR) + input_img.width / 2 * RIGHT + 2 * RIGHT,
            stroke_width=2,
            stroke_color=BLUE,
        )

        trf_title.next_to(trf_line, RIGHT, buff=0)
        trf_title.shift(0.7 * trf_title.height * UP)
        trf_title.shift(trf_title.width * LEFT)

        self.play(Create(trf), run_time=2)
        self.play(Create(trf_line), run_time=0.75)
        self.play(FadeIn(trf_title), run_time=1)

        self.wait(0.5)

        # Last layer receptive field

        erf5 = Rectangle(
            height=3 * cell_width,
            width=3 * cell_width,
            stroke_width=0,
            stroke_color=ORANGE,
            fill_color=ORANGE,
            fill_opacity=1.0,
        )

        erf5.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        # Fourth layer receptive field

        erf4 = Rectangle(
            height=5 * cell_width,
            width=5 * cell_width,
            stroke_width=0,
            stroke_color=ORANGE,
            fill_color=ORANGE,
            fill_opacity=0.5,
        )

        erf4.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        # Third layer receptive field

        erf3 = Rectangle(
            height=7 * cell_width,
            width=7 * cell_width,
            stroke_width=0,
            stroke_color=ORANGE,
            fill_color=ORANGE,
            fill_opacity=0.25,
        )

        erf3.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        # Second layer receptive field

        erf2 = Rectangle(
            height=9 * cell_width,
            width=9 * cell_width,
            stroke_width=0,
            stroke_color=ORANGE,
            fill_color=ORANGE,
            fill_opacity=0.125,
        )

        erf2.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        # First layer receptive field

        erf1 = Rectangle(
            height=11 * cell_width,
            width=11 * cell_width,
            stroke_width=0,
            stroke_color=ORANGE,
            fill_color=ORANGE,
            fill_opacity=0.0625,
        )

        erf1.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        self.wait(0.5)

        self.play(Circumscribe(layer5, color=ORANGE, time_width=0.4), run_time=1)
        self.play(Create(erf5), run_time=1)

        self.play(Circumscribe(layer4, color=ORANGE, time_width=0.4), run_time=1)
        self.play(Create(erf4), run_time=1)

        self.play(Circumscribe(layer3, color=ORANGE, time_width=0.4), run_time=1)
        self.play(Create(erf3), run_time=1)

        self.play(Circumscribe(layer2, color=ORANGE, time_width=0.4), run_time=1)
        self.play(Create(erf2), run_time=1)

        self.play(Circumscribe(layer1, color=ORANGE, time_width=0.4), run_time=1)
        self.play(Create(erf1), run_time=1)

        # Effective receptive field

        erf_title = Tex("Effective Receptive Field", color=ORANGE).scale(0.4)

        erf_line = Line(
            start=erf3.get_corner(UL),
            end=erf3.get_corner(UL) + input_img.width / 2 * LEFT + 2 * LEFT,
            stroke_width=2,
            stroke_color=ORANGE,
        )

        erf_title.next_to(erf_line, LEFT, buff=0)
        erf_title.shift(0.7 * erf_title.height * UP)
        erf_title.shift(erf_title.width * RIGHT)

        self.wait(0.5)

        self.play(Create(erf_line), run_time=1)
        self.play(FadeIn(erf_title), run_time=1)

        self.play(
            FadeOut(erf1, erf2, erf3, erf4, erf5),
            FadeOut(input_img),
            FadeOut(cnn),
            FadeOut(erf_line, erf_title, trf_line, trf_title, trf),
            run_time=2,
        )

        self.wait(2)


# Render the scene
if __name__ == "__main__":

    scene = Scene3_1()
    scene.render()
