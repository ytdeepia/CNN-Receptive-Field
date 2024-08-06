from manim import *
import matplotlib.pyplot as plt
from manim_voiceover import VoiceoverScene
import numpy as np


class Scene3_2(VoiceoverScene, MovingCameraScene):
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
            x_range=[-16, 16],
            y_range=[-16, 16],
            x_length=2,
            y_length=2,
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 0.5,
                "stroke_opacity": 0.5,
            },
            axis_config={
                "stroke_color": GRAY,
                "stroke_width": 0.5,
                "stroke_opacity": 0.5,
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

        # Title screen

        title = Tex("Effective Receptive Field", color=WHITE).scale(1.0)
        line = Underline(title, buff=0.1)

        self.play(Create(title), GrowFromEdge(line, UP), run_time=2)

        # Output feature map

        output_feature = self.create_img("images/feature_one.png")
        feature_14 = self.create_img("images/gradients_cnn20/conv_layers.14_grad.png")

        cell_width = feature_14[0].width / 32

        output_feature_title = Tex("Output Feature Map", color=WHITE).scale(0.8)
        output_feature_title.next_to(output_feature, UP, buff=0.2)

        self.play(FadeOut(title), FadeOut(line), run_time=1)
        self.play(FadeIn(output_feature), Write(output_feature_title), run_time=2)

        self.play(
            output_feature.animate.shift(4 * RIGHT),
            output_feature_title.animate.shift(4 * RIGHT),
            run_time=2,
        )

        feature_14.move_to(ORIGIN + 4 * LEFT)
        feature_14.z_index = 1

        # Plot gradient lines for the first feature map

        line1 = Line(
            end=feature_14.get_center() + 0.5 * cell_width * (DOWN + RIGHT),
            start=output_feature.get_center() + 0.5 * cell_width * (DOWN + RIGHT),
            stroke_width=2,
            color=WHITE,
        )

        rect1 = Rectangle(width=3 * cell_width, height=3 * cell_width, stroke_width=1)
        rect1.move_to(feature_14.get_center() + 0.5 * cell_width * (DOWN + RIGHT))

        self.play(
            LaggedStart(
                ShowPassingFlash(line1, time_width=0.5),
                Create(rect1),
                lag_ratio=0.8,
            ),
            run_time=2,
        )

        feature_14_title = Tex("14th layer", color=WHITE).scale(0.8)
        feature_14_title.next_to(feature_14, UP, buff=0.2)

        self.play(FadeIn(feature_14), Write(feature_14_title), run_time=1)

        # Feature 13

        self.play(
            self.camera.frame.animate.move_to(feature_14.get_center() + LEFT * 4),
            run_time=2,
        )

        feature_13 = self.create_img("images/gradients_cnn20/conv_layers.13_grad.png")
        feature_13.move_to(self.camera.frame_center + 4 * LEFT)
        feature_13.z_index = 1

        line2 = Line(
            end=feature_13.get_center() + 0.5 * cell_width * (DOWN + RIGHT),
            start=feature_14.get_center() + 0.5 * cell_width * (DOWN + RIGHT),
            stroke_width=2,
            color=WHITE,
        )

        rect2 = Rectangle(width=5 * cell_width, height=5 * cell_width, stroke_width=1)
        rect2.move_to(feature_13.get_center() + 0.5 * cell_width * (DOWN + RIGHT))

        self.play(
            LaggedStart(
                ShowPassingFlash(line2, time_width=0.5),
                Create(rect2),
                lag_ratio=0.8,
            ),
            run_time=2,
        )

        feature_13_title = Tex("13th layer", color=WHITE).scale(0.8)
        feature_13_title.next_to(feature_13, UP, buff=0.2)

        self.play(FadeIn(feature_13), Write(feature_13_title), run_time=1)

        # Feature 12

        self.play(
            self.camera.frame.animate.move_to(feature_13.get_center() + LEFT * 4),
            run_time=2,
        )

        feature_12 = self.create_img("images/gradients_cnn20/conv_layers.12_grad.png")

        feature_12.move_to(self.camera.frame_center + 4 * LEFT)
        feature_12.z_index = 1

        line3 = Line(
            end=feature_12.get_center() + 0.5 * cell_width * (DOWN + RIGHT),
            start=feature_13.get_center() + 0.5 * cell_width * (DOWN + RIGHT),
            stroke_width=2,
            color=WHITE,
        )

        rect3 = Rectangle(width=7 * cell_width, height=7 * cell_width, stroke_width=1)
        rect3.move_to(feature_12.get_center() + 0.5 * cell_width * (DOWN + RIGHT))

        self.play(
            LaggedStart(
                ShowPassingFlash(line3, time_width=0.5),
                Create(rect3),
                lag_ratio=0.8,
            ),
            run_time=2,
        )

        feature_12_title = Tex("12th layer", color=WHITE).scale(0.8)
        feature_12_title.next_to(feature_12, UP, buff=0.2)

        self.play(FadeIn(feature_12), Write(feature_12_title), run_time=1)

        # Display the final feature map

        final_feature_map = self.create_img(
            "images/gradients_cnn20/conv_layers.0_grad.png"
        )

        final_feature_map.move_to(feature_12.get_center())

        self.play(
            self.camera.frame.animate.move_to(feature_12.get_center()), run_time=2
        )

        self.play(
            FadeOut(feature_12, rect3),
            FadeOut(feature_12_title),
            FadeOut(feature_13, rect2, feature_13_title),
            FadeIn(final_feature_map),
            run_time=2.0,
        )

        self.remove(
            feature_12,
            rect3,
            feature_12_title,
            feature_13,
            rect2,
            feature_12_title,
            feature_14,
            rect1,
            feature_14_title,
            output_feature,
            output_feature_title,
        )

        final_feature_map_title = Tex("First layer", color=WHITE).scale(0.8)
        final_feature_map_title.next_to(final_feature_map, UP, buff=0.4)

        self.play(Write(final_feature_map_title), run_time=1)

        # Plot theoretical receptive field

        trf_title = Tex("Theoretical Receptive Field", color=BLUE).scale(0.5)

        trf = Rectangle(
            width=32 * cell_width,
            height=32 * cell_width,
            stroke_width=1,
            color=BLUE,
        )

        trf.move_to(final_feature_map.get_center())

        trf_line = Line(
            start=trf.get_corner(DR),
            end=trf.get_corner(DR) + 4 * RIGHT,
            stroke_width=2,
            stroke_color=BLUE,
        )

        trf_title.next_to(trf_line, RIGHT, buff=0)
        trf_title.shift(0.7 * trf_title.height * UP)
        trf_title.shift(trf_title.width * LEFT)

        self.play(Create(trf), run_time=2)
        self.play(Create(trf_line), run_time=0.75)
        self.play(FadeIn(trf_title), run_time=1)

        # Plot effective receptive field

        erf_title = Tex("Effective Receptive Field", color=ORANGE).scale(0.4)

        erf = Rectangle(
            width=18 * cell_width,
            height=18 * cell_width,
            stroke_width=1,
            color=ORANGE,
        )

        erf.move_to(final_feature_map.get_center() + 1 * cell_width * (RIGHT + DOWN))

        erf_line = Line(
            start=erf.get_corner(DL),
            end=erf.get_corner(DL) + 4 * LEFT,
            stroke_width=2,
            stroke_color=ORANGE,
        )

        erf_title.next_to(erf_line, LEFT, buff=0)
        erf_title.shift(0.7 * erf_title.height * UP)
        erf_title.shift(erf_title.width * RIGHT)

        self.play(Create(erf), run_time=2)
        self.play(Create(erf_line), run_time=0.75)
        self.play(FadeIn(erf_title), run_time=1)

        # Display effective receptive field width

        brace_erf = Brace(erf, direction=RIGHT, color=ORANGE, buff=1)
        brace_erf_text = (
            brace_erf.get_text(
                "18",
                buff=0.1,
            )
            .scale(0.5)
            .set_color(ORANGE)
        )

        self.play(Create(brace_erf), FadeIn(brace_erf_text), run_time=1)

        self.wait(0.5)

        # Show the receptive field with uniform weights

        uniform_weights = self.create_img(
            "images/gradients_cnn20uniform/conv_layers.0_grad.png"
        )
        uniform_weights.move_to(final_feature_map.get_center())
        uniform_weights.z_index = -1

        self.play(
            FadeOut(final_feature_map),
            FadeOut(trf, trf_line, trf_title),
            FadeOut(erf, erf_line, erf_title, brace_erf, brace_erf_text),
            FadeIn(uniform_weights),
            run_time=2,
        )

        self.wait(0.5)

        self.play(FadeOut(uniform_weights, final_feature_map_title), run_time=2)

        self.wait(2)


# Render the scene
if __name__ == "__main__":

    scene = Scene3_2()
    scene.render()
