from manim import *

class NumberAnimation(Scene):
    def construct(self):
        # Create a ValueTracker to track the value of the number
        number_tracker = ValueTracker(7)

        # Create a DecimalNumber and link it to the tracker
        number = DecimalNumber(number_tracker.get_value()).set_color(WHITE)
        number.add_updater(lambda v: v.set_value(number_tracker.get_value()))

        # Add the number to the scene
        self.add(number)

        # Animate the change from 7 to 100
        self.play(number_tracker.animate.set_value(100), run_time=5, rate_func=linear)

        # Hold the final value to let the audience see the result
        self.wait(1)
