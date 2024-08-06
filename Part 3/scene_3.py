from manim import *
import matplotlib.pyplot as plt
from manim_voiceover import VoiceoverScene
import numpy as np


class Scene3_3(VoiceoverScene, MovingCameraScene):
    def create_layer(self, n_filters=3):

        layer = VGroup()

        for i in range(n_filters):
            f = Rectangle(
                height=1,
                width=1,
                fill_color=random_bright_color(),
                fill_opacity=1,
                stroke_width=0,
            )

            layer.add(f)

        layer.arrange(DOWN + RIGHT, buff=-0.9 * f.height)

        return layer

    def create_connected_layers(self):

        # First column

        first_column = VGroup(
            *[Circle(radius=0.05, color=WHITE, stroke_width=0.8) for _ in range(3)],
            *[Dot(color=WHITE, radius=0.02) for _ in range(3)],
            *[Circle(radius=0.05, color=WHITE, stroke_width=0.8) for _ in range(3)],
        )

        first_column.arrange(DOWN, buff=0.1)

        # Second column configuration
        second_column = VGroup(
            *[Circle(radius=0.05, color=WHITE, stroke_width=0.8) for _ in range(3)],
            *[Dot(color=WHITE, radius=0.02) for _ in range(3)],
            *[Circle(radius=0.05, color=WHITE, stroke_width=0.8) for _ in range(3)],
        )

        second_column.arrange(DOWN, buff=0.05).next_to(first_column, RIGHT, buff=0.7)

        # Draw lines from each circle in the first column to each circle in the second column
        lines1 = VGroup()
        for first_elem in first_column:
            if not isinstance(first_elem, Dot):  # Check to only connect circles
                for second_elem in second_column:
                    if not isinstance(
                        second_elem, Dot
                    ):  # Check to only connect circles
                        line = Line(
                            first_elem.get_right(),
                            second_elem.get_left(),
                            stroke_width=0.5,
                            color=GREY,
                        )
                        lines1.add(line)

        # Third column configuration
        third_column = VGroup(
            *[Circle(radius=0.05, color=WHITE, stroke_width=0.8) for _ in range(10)]
        )
        third_column.arrange(DOWN, buff=0.05).next_to(second_column, RIGHT, buff=0.7)

        # Draw lines from each circle in the second column to each circle in the third column
        lines2 = VGroup()
        for second_elem in second_column:
            if not isinstance(second_elem, Dot):  # Check to only connect circles
                for third_elem in third_column:
                    line = Line(
                        second_elem.get_right(),
                        third_elem.get_left(),
                        stroke_width=0.5,
                        color=GREY,
                    )
                    lines2.add(line)

        network = VGroup(first_column, second_column, third_column, lines1, lines2)

        return network

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

        # Lenet-5 architecture

        layer1 = self.create_layer(n_filters=6)
        layer2 = self.create_layer(n_filters=6).scale(0.5)
        layer3 = self.create_layer(n_filters=16).scale(0.5)
        layer4 = self.create_layer(n_filters=16).scale(0.25)
        fc_layers = self.create_connected_layers().scale(1.5)

        layer1.to_edge(LEFT, buff=1)
        layer2.next_to(layer1, RIGHT, buff=1)
        layer3.next_to(layer2, RIGHT, buff=1)
        layer4.next_to(layer3, RIGHT, buff=1)
        fc_layers.next_to(layer4, RIGHT, buff=1)

        arrow1 = Arrow(
            layer1.get_right(),
            layer2.get_left(),
            color=WHITE,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )
        arrow2 = Arrow(
            layer2.get_right(),
            layer3.get_left(),
            color=WHITE,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )
        arrow3 = Arrow(
            layer3.get_right(),
            layer4.get_left(),
            color=WHITE,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )
        arrow4 = Arrow(
            layer4.get_right(),
            fc_layers.get_left(),
            color=WHITE,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
        )

        lenet = VGroup(
            layer1,
            layer2,
            layer3,
            layer4,
            fc_layers,
            arrow1,
            arrow2,
            arrow3,
            arrow4,
        )

        lenet.move_to(ORIGIN).scale(0.8)

        self.play(
            LaggedStart(
                Create(layer1),
                GrowArrow(arrow1),
                Create(layer2),
                GrowArrow(arrow2),
                Create(layer3),
                GrowArrow(arrow3),
                Create(layer4),
                GrowArrow(arrow4),
                Create(fc_layers),
                lag_ratio=0.8,
            ),
            run_time=5,
        )

        # LeNet-5 title

        lenet_title = Tex("LeNet-5", color=WHITE).next_to(lenet, DOWN, buff=0.5)
        lenet_title_underline = Underline(lenet_title, buff=0.1)
        self.play(
            Write(lenet_title),
            GrowFromPoint(lenet_title_underline, lenet_title_underline.get_left()),
            run_time=1,
        )

        # Discard fully connected layers
        lenet.remove(fc_layers, arrow4)

        self.play(
            LaggedStart(
                FadeOut(fc_layers),
                FadeOut(arrow4),
                lenet.animate.move_to(ORIGIN),
                lag_ratio=0.4,
            ),
            run_time=4,
        )

        lenet.add(lenet_title, lenet_title_underline)
        self.play(lenet.animate.to_edge(DOWN, buff=0.3), run_time=1.5)

        # Untrained receptive field

        untrained_erf = self.create_img("images/erf_untrained.png").scale(0.8)
        untrained_erf.to_edge(UP, buff=1.5)

        untrained_erf_title = (
            Tex("Effective Receptive Field", color=WHITE)
            .next_to(untrained_erf, UP, buff=0.5)
            .scale(0.8)
        )

        self.play(FadeIn(untrained_erf), Write(untrained_erf_title), run_time=1)

        # Trained receptive field

        trained_erfs = []
        for i in range(1, 21, 1):
            trained_erf = self.create_img(f"images/erf_trained_{i}.png").scale(0.8)
            trained_erf.to_edge(UP, buff=1.5)

            trained_erfs.append(trained_erf)

        title_target = Tex("Epoch 1").scale(0.8).next_to(untrained_erf, UP, buff=0.5)

        self.play(
            FadeOut(untrained_erf),
            Transform(untrained_erf_title, title_target),
            FadeIn(trained_erfs[0]),
        )

        for i in range(2, 11, 1):
            title_target = (
                Tex(f"Epoch {i}").scale(0.8).next_to(untrained_erf, UP, buff=0.5)
            )
            self.play(
                FadeOut(trained_erfs[i - 2]),
                Transform(untrained_erf_title, title_target),
                FadeIn(trained_erfs[i - 1]),
                run_time=0.5,
            )
            self.wait(0.5)

        for i in range(11, 21, 1):
            title_target = (
                Tex(f"Epoch {i}").scale(0.8).next_to(untrained_erf, UP, buff=0.5)
            )
            self.play(
                FadeOut(trained_erfs[i - 2]),
                Transform(untrained_erf_title, title_target),
                FadeIn(trained_erfs[i - 1]),
                run_time=0.5,
            )
            self.wait(0.5)

        # Display accuracy

        self.play(FadeOut(lenet, lenet_title, lenet_title_underline), run_time=1)

        accuracy = (
            Tex("Top-1 Classification: 98.6\\%", color=WHITE)
            .scale(1.2)
            .to_edge(DOWN, buff=1.0)
        )
        self.play(Write(accuracy), run_time=1)
        self.play(Circumscribe(accuracy, color=WHITE), run_time=1)

        self.play(
            FadeOut(accuracy),
            FadeOut(trained_erfs[19], untrained_erf_title),
            run_time=2,
        )

        self.wait(2)


# Render the scene
if __name__ == "__main__":

    scene = Scene3_3()
    scene.render()
