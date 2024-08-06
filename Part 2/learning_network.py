from manim import *
import random

class NeuralNetworkLearning(Scene):
    def construct(self):
        # Title
        title = Text("Neural Network Learning").to_edge(UP)
        self.play(Write(title))
        
        # Create a neural network structure
        input_layer = self.create_layer(3, 0.1, LEFT)
        hidden_layer = self.create_layer(4, 0.1, ORIGIN)
        output_layer = self.create_layer(2, 0.1, RIGHT)
        
        layers = [input_layer, hidden_layer, output_layer]
        
        # Draw the layers
        for layer in layers:
            self.play(Create(layer), run_time=0.5)

        # Create connections between layers
        connections = self.connect_layers(input_layer, hidden_layer) + self.connect_layers(hidden_layer, output_layer)
        
        for connection in connections:
            self.play(Create(connection), run_time=0.1)
        
        # Simulate learning by updating weights
        self.simulate_learning(connections)

    def create_layer(self, num_neurons, neuron_radius, position):
        neurons = VGroup(*[Circle(radius=neuron_radius) for _ in range(num_neurons)])
        neurons.arrange(DOWN, buff=0.5)
        neurons.move_to(position)
        return neurons
    
    def connect_layers(self, layer1, layer2):
        connections = []
        for neuron1 in layer1:
            for neuron2 in layer2:
                connection = Line(neuron1.get_right(), neuron2.get_left())
                connections.append(connection)
        return connections

    def simulate_learning(self, connections):
        # Simulate weight updates by changing the color of connections
        for i in range(20):
            # Select a connection at random
            random_connection = random.choice(connections)

            # Simulate weight updates by changing the color of the selected connection
            self.play(random_connection.animate.set_color(YELLOW), run_time=0.1)
            self.play(random_connection.animate.set_color(WHITE), run_time=0.1)

# To render the scene, use the following command in the terminal:
# manim -pql script_name.py NeuralNetworkLearning
