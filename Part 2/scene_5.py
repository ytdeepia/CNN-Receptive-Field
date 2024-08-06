from manim import *
import matplotlib.pyplot as plt
from manim_voiceover import VoiceoverScene
import numpy as np


class Scene2_5(VoiceoverScene, ThreeDScene):
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

    def create_pooling_layer(self):
        pooling_layer = Rectangle(
            height=1,
            width=1,
            fill_color=RED,
            fill_opacity=1,
            color=WHITE,
            stroke_width=2,
        )
        line1 = Line(
            pooling_layer.get_top(),
            pooling_layer.get_bottom(),
            color=WHITE,
            stroke_width=2,
        )
        line2 = Line(
            pooling_layer.get_left(),
            pooling_layer.get_right(),
            color=WHITE,
            stroke_width=2,
        )

        pooling_layer = VGroup(pooling_layer, line1, line2)

        return pooling_layer

    def create_img(self, img_path, size=28):
        img = (
            ImageMobject(img_path)
            .set_resampling_algorithm(RESAMPLING_ALGORITHMS["none"])
            .scale(15)
        )

        lattice = NumberPlane(
            x_range=[-size // 2, size // 2],
            y_range=[-size // 2, size // 2],
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

        # Images and their lattice

        input_img = self.create_img("images/0_mnist.png", size=28)
        pooled_img = self.create_img("images/0_mnist_pooled.png", size=14).scale(2)

        input_img_ttl = Tex("Input Image").scale(0.5)
        input_img_ttl.next_to(input_img, UP, buff=0.1)

        pooled_img_ttl = Tex("Pooled Image").scale(0.5)

        input_img_obj = Group(input_img, input_img_ttl)
        pooled_img_obj = Group(pooled_img, pooled_img_ttl)

        cell_width = input_img[0].width / 28

        # Pooling layer

        pooling_layer = self.create_pooling_layer()

        input_img.move_to(ORIGIN)
        pooling_layer.next_to(input_img, RIGHT, buff=1.5)
        pooled_img.next_to(pooling_layer, RIGHT, buff=1.5)
        pooled_img_ttl.next_to(pooled_img, UP, buff=0.1)

        pooling_layer_brace = Brace(pooling_layer, direction=UP, color=WHITE, buff=0.2)
        pooling_layer_ttl = pooling_layer_brace.get_text("Max pooling").scale(0.5)

        arrow1 = Arrow(
            input_img.get_right(),
            pooling_layer.get_left(),
            color=WHITE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow2 = Arrow(
            pooling_layer.get_right(),
            pooled_img.get_left(),
            color=WHITE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        pooling_obj = Group(
            input_img_obj,
            pooling_layer,
            pooling_layer_brace,
            pooling_layer_ttl,
            pooled_img_obj,
            arrow1,
            arrow2,
        )
        pooling_obj.move_to(ORIGIN + DOWN)

        self.play(
            LaggedStart(
                FadeIn(input_img_obj),
                GrowArrow(arrow1),
                FadeIn(pooling_layer, pooling_layer_brace, pooling_layer_ttl),
                GrowArrow(arrow2),
                FadeIn(pooled_img_obj),
                lag_ratio=0.3,
            ),
            run_time=2,
        )

        self.wait(0.5)

        # Move input image to upper right corner

        self.play(
            FadeOut(
                arrow1,
                arrow2,
                pooling_layer,
                pooled_img_obj,
                pooling_layer_brace,
                pooling_layer_ttl,
            ),
            run_time=1,
        )

        self.play(input_img_obj.animate.to_corner(UR, buff=1.0), run_time=1)

        # Formula

        formula = formula = MathTex(
            "r_0 =",
            "\\sum_{l = 1}^{L}",
            "\\left(",
            "(k_l - 1)",
            "\\prod_{i=1}^{l-1}",
            "s_i",
            "\\right)",
            "+",
            "1",
        ).scale(0.8)

        formula.to_corner(UL, buff=2.0)
        formula_title = Tex("Receptive Field").scale(0.5)
        formula_title.next_to(formula, UP, buff=0.8)

        self.play(
            LaggedStart(Write(formula), FadeIn(formula_title), lag_ratio=0.3),
            run_time=1,
        )

        # Highlight product

        prod_rect = SurroundingRectangle(
            formula[4:6], color=RED, stroke_width=4, buff=0.1
        )

        self.play(Create(prod_rect), run_time=1)

        # Simplify formula

        simplified_formula = (
            MathTex("r_0 =", "2^P", "\\sum_{l = 1}^{L}", "(k_l - 1)", "+", "1")
            .scale(0.8)
            .move_to(formula)
        )

        self.wait(0.7)

        self.wait(2)

        self.play(
            FadeOut(prod_rect),
            ReplacementTransform(formula, simplified_formula),
            run_time=1,
        )

        p_txt = Tex("P = Number of pooling layers").scale(0.5)
        p_txt.next_to(simplified_formula, DOWN, buff=1.0)

        self.play(Write(p_txt), run_time=1)

        self.play(Indicate(simplified_formula[1], color=RED), run_time=2)

        self.play(Indicate(simplified_formula[1], color=RED), run_time=2)

        self.wait(0.5)

        # CNN with pooling

        layer1 = self.create_layer()
        pooling_layer1 = self.create_pooling_layer()
        layer2 = self.create_layer()
        pooling_layer2 = self.create_pooling_layer()
        layer3 = self.create_layer()
        pooling_layer3 = self.create_pooling_layer()

        pooling_layer1.next_to(layer1, RIGHT, buff=0.2)
        layer2.next_to(pooling_layer1, RIGHT, buff=1.0)
        pooling_layer2.next_to(layer2, RIGHT, buff=0.2)
        layer3.next_to(pooling_layer2, RIGHT, buff=1.0)
        pooling_layer3.next_to(layer3, RIGHT, buff=0.2)

        arrow1 = Arrow(
            pooling_layer1.get_right(),
            layer2.get_left(),
            color=WHITE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )
        arrow2 = Arrow(
            pooling_layer2.get_right(),
            layer3.get_left(),
            color=WHITE,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.15,
        )

        cnn = VGroup(
            layer1,
            pooling_layer1,
            arrow1,
            layer2,
            pooling_layer2,
            arrow2,
            layer3,
            pooling_layer3,
        )

        cnn.move_to(ORIGIN)
        cnn.to_edge(DOWN, buff=1.0)

        brace1 = Brace(layer1, direction=DOWN, color=WHITE, buff=0.1)
        brace1_txt = brace1.get_text("3x3 Filter").scale(0.4)

        brace_pool1 = Brace(pooling_layer1, direction=DOWN, color=WHITE, buff=0.1)
        brace_pool1_txt = brace_pool1.get_text("Max Pooling").scale(0.4)

        brace2 = Brace(layer2, direction=DOWN, color=WHITE, buff=0.1)
        brace2_txt = brace2.get_text("3x3 Filter").scale(0.4)

        brace_pool2 = Brace(pooling_layer2, direction=DOWN, color=WHITE, buff=0.1)
        brace_pool2_txt = brace_pool2.get_text("Max Pooling").scale(0.4)

        brace3 = Brace(layer3, direction=DOWN, color=WHITE, buff=0.05)
        brace3_txt = brace3.get_text("3x3 Filter").scale(0.4)

        brace_pool3 = Brace(pooling_layer3, direction=DOWN, color=WHITE, buff=0.1)
        brace_pool3_txt = brace_pool3.get_text("Max Pooling").scale(0.4)

        self.play(
            LaggedStart(
                FadeIn(
                    layer1,
                    pooling_layer1,
                    brace1,
                    brace1_txt,
                    brace_pool1,
                    brace_pool1_txt,
                ),
                GrowArrow(arrow1),
                FadeIn(
                    layer2,
                    pooling_layer2,
                    brace2,
                    brace2_txt,
                    brace_pool2,
                    brace_pool2_txt,
                ),
                GrowArrow(arrow2),
                FadeIn(
                    layer3,
                    pooling_layer3,
                    brace3,
                    brace3_txt,
                    brace_pool3,
                    brace_pool3_txt,
                ),
                lag_ratio=0.4,
            ),
            run_time=tracker.duration / 2,
        )

        # Highlight first layer and create receptive field

        self.play(Circumscribe(layer1, color=ORANGE, stroke_width=2), run_time=2)

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

        self.play(Create(receptive_field_rect), run_time=2)

        # Highlight first pooling layer

        self.play(
            Circumscribe(pooling_layer1, color=ORANGE, stroke_width=2), run_time=1
        )
        self.play(
            receptive_field_rect.animate.scale_to_fit_height(6 * cell_width).shift(
                0.5 * cell_width * LEFT + 0.5 * cell_width * DOWN
            ),
            run_time=0.5,
        )

        # Highlight second layer

        self.play(Circumscribe(layer2, color=ORANGE, stroke_width=2), run_time=1)
        self.play(
            receptive_field_rect.animate.scale_to_fit_height(7 * cell_width).shift(
                0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
            ),
            run_time=0.5,
        )

        # Highlight second pooling layer

        self.play(
            Circumscribe(pooling_layer2, color=ORANGE, stroke_width=2), run_time=1
        )
        self.play(
            receptive_field_rect.animate.scale_to_fit_height(14 * cell_width).shift(
                0.5 * cell_width * LEFT + 0.5 * cell_width * DOWN
            ),
            run_time=0.5,
        )

        # Highlight third layer

        self.play(Circumscribe(layer3, color=ORANGE, stroke_width=2), run_time=1)
        self.play(
            receptive_field_rect.animate.scale_to_fit_height(15 * cell_width).shift(
                0.5 * cell_width * RIGHT + 0.5 * cell_width * UP
            ),
            run_time=0.5,
        )

        # Highlight third pooling layer

        self.play(
            Circumscribe(pooling_layer3, color=ORANGE, stroke_width=2), run_time=1
        )
        self.play(
            receptive_field_rect.animate.scale_to_fit_height(28 * cell_width).shift(
                0.5 * cell_width * LEFT + 0.5 * cell_width * DOWN
            ),
            run_time=0.5,
        )

        # Replace with a HQ image

        hq_img = ImageMobject("images/dog.jpg").scale(0.35)
        hq_img_rect = SurroundingRectangle(hq_img, color=GRAY, stroke_width=1, buff=0)
        hq_img = Group(hq_img, hq_img_rect)
        hq_img.move_to(input_img)

        self.wait(0.6)

        self.play(
            FadeOut(receptive_field_rect, input_img_obj), FadeIn(hq_img), run_time=2
        )

        self.wait(0.5)

        # Replace layer with multiple layers

        dots = Tex("...").scale(1.2)
        layer2_obj = VGroup(layer2, pooling_layer2)
        dots.move_to(layer2_obj.get_center())
        cnn.remove(layer2, pooling_layer2)
        cnn.add(dots)

        dots_brace = Brace(layer2_obj, direction=DOWN, color=WHITE, buff=0.05)
        dots_brace_txt = dots_brace.get_text("8 layers").scale(0.5)

        self.play(
            FadeOut(
                layer2,
                pooling_layer2,
                brace2,
                brace2_txt,
                brace_pool2,
                brace_pool2_txt,
            ),
            FadeIn(dots, dots_brace, dots_brace_txt),
            run_time=1,
        )

        # Draw receptive field around the dog

        receptive_field_rect = Rectangle(
            height=1.9, width=1.9, color=ORANGE, fill_opacity=0.2, stroke_width=2
        )
        receptive_field_rect.move_to(hq_img.get_center() + 0.1 * RIGHT + 0.1 * DOWN)

        self.play(Create(receptive_field_rect), run_time=1)

        self.play(
            FadeOut(receptive_field_rect, hq_img, cnn, dots_brace, dots_brace_txt),
            FadeOut(
                brace1,
                brace1_txt,
                brace_pool1,
                brace_pool1_txt,
                brace3,
                brace3_txt,
                brace_pool3,
                brace_pool3_txt,
            ),
            FadeOut(formula_title, simplified_formula, p_txt),
            run_time=2,
        )

        self.wait(2)


# Render the scene
if __name__ == "__main__":

    scene = Scene2_5()
    scene.render()
