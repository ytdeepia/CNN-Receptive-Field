from manim import *
import matplotlib.pyplot as plt
from manim_voiceover import VoiceoverScene
import numpy as np


class Scene1_1(VoiceoverScene, ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            image_frame_stroke_width=2,
            zoomed_camera_config={
                "default_frame_stroke_width": 2,
            },
            **kwargs,
        )

    def create_matrix_filter(self, matrix_content):
        matrix_grid = NumberPlane(
            x_range=[-1, 2],
            y_range=[-1, 2],
            x_length=2,
            y_length=2,
            background_line_style={
                "stroke_color": GRAY,
                "stroke_width": 2,
                "stroke_opacity": 1,
            },
            axis_config={
                "stroke_color": GRAY,
                "stroke_width": 2,
                "include_numbers": False,
            },
            faded_line_ratio=0,
        ).move_to(ORIGIN)

        # Directly using x_length and y_length for rectangle
        rectangle = Rectangle(width=2, height=2, color=GRAY, stroke_width=2).move_to(
            ORIGIN
        )
        cell_width_filter = matrix_grid.get_x_unit_size()

        filter_text = VGroup()
        for i in range(3):
            for j in range(3):
                coords = matrix_grid.coords_to_point(j, i)
                val = matrix_content[j][i]
                text = Tex(f"{val:.2f}", color=BLUE)
                text.move_to(
                    coords + LEFT * cell_width_filter / 2 + DOWN * cell_width_filter / 2
                ).scale(0.5)
                filter_text.add(text)

        return VGroup(matrix_grid, rectangle, filter_text)

    def construct(self):

        self.wait(2)

        # Set up image
        image = (
            ImageMobject("images/0_mnist.png")
            .set_resampling_algorithm(RESAMPLING_ALGORITHMS["none"])
            .scale(20)
        )
        image_rect = SurroundingRectangle(image, buff=0, stroke_width=2, color=WHITE)
        lattice = NumberPlane(
            x_range=(-14, 14, 1),
            y_range=(-14, 14, 1),
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
            faded_line_ratio=0,  # Disable fading of grid lines
        )

        lattice.scale(image.height / lattice.height)

        image = Group(image, lattice, image_rect)

        # Set up zoomed camera

        zoomed_camera = self.zoomed_camera
        frame = zoomed_camera.frame

        zoomed_display = self.zoomed_display
        zoomed_display.scale_to_fit_height(image.height)
        zoomed_display.scale_to_fit_width(image.width)
        zoomed_display.move_to(ORIGIN)
        zoomed_display.shift(RIGHT * 3)
        zoomed_display_frame = zoomed_display.display_frame

        zd_rect = BackgroundRectangle(
            zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF
        )

        unfold_camera = UpdateFromFunc(
            zd_rect, lambda rect: rect.replace(zoomed_display)
        )

        cell_width = image.height / 28
        frame.scale_to_fit_height(3 * cell_width)
        frame.scale_to_fit_width(3 * cell_width)

        # Animate image

        self.play(FadeIn(image))
        self.wait()

        self.wait(0.3)

        image_title = Tex("What you see", color=WHITE)
        image_title.next_to(image, UP, buff=0.5)

        self.play(Write(image_title))
        self.play(ApplyWave(image_title))

        self.wait(0.3)

        self.play(
            image.animate.shift(3 * LEFT),
            image_title.animate.shift(3 * LEFT),
        )
        self.wait()

        frame.move_to(
            image.get_corner(UL) + DOWN * 0.5 * cell_width + RIGHT * 0.5 * cell_width
        )
        frame.shift(RIGHT * 14 * cell_width + DOWN * 3 * cell_width)

        self.wait(0.3)

        # Animate zoomed camera creation

        self.play(Create(frame))
        self.wait()

        self.play(
            self.get_zoomed_display_pop_out_animation(),
            unfold_camera,
        )

        self.activate_zooming()

        zoomed_title = Tex("What the filter sees", color=WHITE)
        zoomed_title.next_to(zoomed_display, UP, buff=0.5)
        self.play(Write(zoomed_title))

        self.wait(0.3)

        # Move camera around

        self.play(frame.animate.shift(RIGHT * cell_width), run_time=1)
        self.play(frame.animate.shift(RIGHT * cell_width), run_time=1)
        self.play(frame.animate.shift(RIGHT * cell_width), run_time=1)
        self.play(frame.animate.shift(DOWN * cell_width), run_time=1)

        self.wait(0.3)

        self.play(frame.animate.scale_to_fit_width(5 * cell_width), run_time=1)
        self.play(frame.animate.shift(UP * cell_width), run_time=1)
        self.play(frame.animate.shift(LEFT * cell_width), run_time=1)
        self.play(frame.animate.shift(LEFT * cell_width), run_time=1)
        self.play(frame.animate.shift(DOWN * cell_width), run_time=1)
        self.play(frame.animate.scale_to_fit_width(7 * cell_width), run_time=1)
        self.play(frame.animate.shift(DOWN * cell_width), run_time=1)
        self.play(frame.animate.shift(RIGHT * cell_width), run_time=1)

        self.wait(0.3)

        # Fade Out everything
        self.play(
            FadeOut(image),
            FadeOut(image_title),
            FadeOut(zoomed_title),
            FadeOut(frame),
            FadeOut(zoomed_display_frame),
            FadeOut(zd_rect),
        )

        self.wait(2)


# Render the scene
if __name__ == "__main__":

    scene = Scene1_1()
    scene.render()
