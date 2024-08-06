from manim import *
import matplotlib.pyplot as plt
from manim_voiceover import VoiceoverScene
import numpy as np


class Scene2_4(VoiceoverScene, ThreeDScene):
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

        image_title = Tex("Input Image").scale(0.5)
        image_title.next_to(input_img, UP, buff=0.1)

        input_img_obj = Group(input_img, image_title)
        input_img_obj.to_corner(UR, buff=0.5)
        input_img_obj.shift(1.0 * LEFT)

        cell_width = input_img[0].width / 28

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

        self.play(FadeIn(input_img_obj), run_time=1)

        self.play(
            LaggedStart(
                FadeIn(layer1, brace1),
                GrowArrow(arrow1),
                FadeIn(layer2, brace2),
                GrowArrow(arrow2),
                FadeIn(layer3, brace3),
                lag_ratio=0.2,
            ),
            run_time=2,
        )

        # Formula

        formula = MathTex(
            r"r_0 = \sum_{l = 1}^{L} \left(  (k_l - 1) \prod_{i=1}^{l-1} s_i \right) + 1"
        ).scale(0.8)
        formula.to_corner(UL, buff=2.0)
        formula_title = Tex("Receptive Field").scale(0.5)
        formula_title.next_to(formula, UP, buff=0.8)

        self.play(
            LaggedStart(Write(formula), FadeIn(formula_title), lag_ratio=0.3),
            run_time=1,
        )

        rect = SurroundingRectangle(layer1, color=ORANGE, stroke_width=4, buff=0.1)
        self.play(ShowPassingFlash(rect, time_width=0.3), run_time=2)

        receptive_field_rect = Rectangle(
            height=3 * cell_width,
            width=3 * cell_width,
            color=ORANGE,
            fill_opacity=0.2,
            stroke_width=2,
        )
        receptive_field_rect.move_to(
            input_img.get_center() + 0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
        )

        self.play(Create(receptive_field_rect), run_time=1)

        # Highlight each layer

        rect = SurroundingRectangle(layer2, color=ORANGE, stroke_width=4, buff=0.1)
        self.play(ShowPassingFlash(rect, time_width=0.3), run_time=2)

        self.play(receptive_field_rect.animate.scale_to_fit_width(5 * cell_width))

        rect = SurroundingRectangle(layer3, color=ORANGE, stroke_width=4, buff=0.1)
        self.play(ShowPassingFlash(rect, time_width=0.3), run_time=2)

        self.play(receptive_field_rect.animate.scale_to_fit_width(7 * cell_width))

        # Simplify formula

        formula_target = MathTex(r"r_0 = 2 \times L + 1").scale(0.8)

        formula_target.move_to(formula)

        self.play(Transform(formula, formula_target))

        # Bounding box of the digit

        digit_rect = Rectangle(
            height=19 * cell_width,
            width=19 * cell_width,
            color=BLUE,
            fill_opacity=0,
            stroke_width=2,
        )
        digit_rect.move_to(
            receptive_field_rect.get_center()
            + 0.5 * cell_width * RIGHT
            + 0.5 * cell_width * LEFT
        )

        line_digit_rect = Line(
            digit_rect.get_corner(UL),
            digit_rect.get_corner(UL) + 1.0 * LEFT,
            color=BLUE,
            stroke_width=2,
        )
        line_digit_txt = Tex("Digit", color=BLUE).scale(0.5)
        line_digit_txt.next_to(line_digit_rect, LEFT, buff=0.1)

        self.play(
            LaggedStart(
                Create(digit_rect),
                Create(line_digit_rect),
                Write(line_digit_txt),
                lag_ratio=0.75,
            ),
            run_time=2,
        )

        # Add layers to the CNN

        dots = Tex("...").scale(0.8)
        dots.move_to(layer2.get_center())
        cnn.remove(layer2)
        cnn.add(dots)

        txt2_target = brace2[0].get_text("2 layers").scale(0.5)

        self.play(
            LaggedStart(
                FadeOut(layer2),
                FadeIn(dots),
                Transform(txt2, txt2_target),
                receptive_field_rect.animate.scale_to_fit_width(9 * cell_width),
                lag_ratio=0.5,
            ),
            run_time=1,
        )

        # Grow the receptive field to the size of the digit

        txt2_target = brace2[0].get_text("3 layers").scale(0.5)

        self.play(
            LaggedStart(
                Transform(txt2, txt2_target),
                receptive_field_rect.animate.scale_to_fit_width(11 * cell_width),
                lag_ratio=0.2,
            ),
            run_time=1.2,
        )

        txt2_target = brace2[0].get_text("4 layers").scale(0.5)

        self.play(
            LaggedStart(
                Transform(txt2, txt2_target),
                receptive_field_rect.animate.scale_to_fit_width(13 * cell_width),
                lag_ratio=0.2,
            ),
            run_time=1.2,
        )

        txt2_target = brace2[0].get_text("5 layers").scale(0.5)

        self.play(
            LaggedStart(
                Transform(txt2, txt2_target),
                receptive_field_rect.animate.scale_to_fit_width(15 * cell_width),
                lag_ratio=0.2,
            ),
            run_time=1.2,
        )

        txt2_target = brace2[0].get_text("6 layers").scale(0.5)

        self.play(
            LaggedStart(
                Transform(txt2, txt2_target),
                receptive_field_rect.animate.scale_to_fit_width(17 * cell_width),
                lag_ratio=0.2,
            ),
            run_time=1.2,
        )

        txt2_target = brace2[0].get_text("7 layers").scale(0.5)

        self.play(
            LaggedStart(
                Transform(txt2, txt2_target),
                receptive_field_rect.animate.scale_to_fit_width(19 * cell_width),
                lag_ratio=0.2,
            ),
            run_time=1.2,
        )

        # Replace the image with a high quality one

        hq_img = ImageMobject("images/dog.jpg").scale(0.35)
        hq_img_rect = SurroundingRectangle(hq_img, color=GRAY, stroke_width=1, buff=0)
        hq_img = Group(hq_img, hq_img_rect)
        hq_img.move_to(input_img)

        self.play(
            FadeOut(
                input_img,
                receptive_field_rect,
                digit_rect,
                line_digit_rect,
                line_digit_txt,
            ),
            run_time=2,
        )

        self.play(FadeIn(hq_img), run_time=2)

        # Add bounding box of the dog

        dog_rect = Rectangle(
            height=18 * cell_width,
            width=18 * cell_width,
            color=BLUE,
            fill_opacity=0,
            stroke_width=2,
        )
        dog_rect.move_to(hq_img.get_center())

        line_dog_rect = Line(
            dog_rect.get_corner(UL),
            dog_rect.get_corner(UL) + 1.0 * LEFT,
            color=BLUE,
            stroke_width=2,
        )
        line_dog_txt = Tex("Dog", color=BLUE).scale(0.5)
        line_dog_txt.next_to(line_dog_rect, LEFT, buff=0.1)

        self.play(
            LaggedStart(
                Create(dog_rect),
                Create(line_dog_rect),
                Write(line_dog_txt),
                lag_ratio=0.75,
            ),
            run_time=2,
        )

        self.wait(1)

        text2_target = brace2[0].get_text("100+ layers").scale(0.5)

        self.play(Transform(txt2, text2_target), run_time=1)

        self.wait(0.7)

        # FadeOut everything

        self.play(
            FadeOut(
                hq_img,
                image_title,
                dog_rect,
                line_dog_rect,
                line_dog_txt,
                txt2,
                cnn,
                formula,
                formula_title,
            ),
            run_time=2,
        )

        txt = Tex("Pooling Layers")

        self.play(Write(txt), run_time=2)

        self.wait(1)

        self.play(Flash(txt, flash_radius=0.8 * txt.width, line_length=1.0), run_time=1)

        self.wait(2)


# Render the scene
if __name__ == "__main__":

    scene = Scene2_4()
    scene.render()
