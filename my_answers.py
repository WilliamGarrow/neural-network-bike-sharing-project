import numpy as np


class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights
        self.weights_input_to_hidden = np.random.normal(0.0, self.input_nodes**-0.5,
                                       (self.input_nodes, self.hidden_nodes))

        self.weights_hidden_to_output = np.random.normal(0.0, self.hidden_nodes**-0.5,
                                       (self.hidden_nodes, self.output_nodes))
        self.lr = learning_rate

        #### COMPLETED: Set self.activation_function to your implemented sigmoid function ####
        #
        # Note: in Python, you can define a function with a lambda expression,
        # as shown below.

        ## Sigmoid notes from Gradient Descent - Lectures 2_2_10-13
        self.activation_function = lambda x : 1 / (1 + np.exp(-x))  # Replace 0 with your sigmoid calculation.

        ### If the lambda code above is not something you're familiar with,
        # You can uncomment out the following three lines and put your
        # implementation there instead.
        #
        #def sigmoid(x):
        #    return 1 / (1 + np.exp(-x))  # Replace 0 with your sigmoid calculation here
        #self.activation_function = sigmoid


    def train(self, features, targets):
        ''' Train the network on batch of features and targets.

            Arguments
            ---------

            features: 2D array, each row is one data record, each column is a feature
            targets: 1D array of target values

        '''
        n_records = features.shape[0]
        delta_weights_i_h = np.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = np.zeros(self.weights_hidden_to_output.shape)
        for X, y in zip(features, targets):

            final_outputs, hidden_outputs = self.forward_pass_train(X)  # Implement the forward pass function below
            # Implement the backproagation function below
            delta_weights_i_h, delta_weights_h_o = self.backpropagation(final_outputs, hidden_outputs, X, y,
                                                                        delta_weights_i_h, delta_weights_h_o)
        self.update_weights(delta_weights_i_h, delta_weights_h_o, n_records)


    def forward_pass_train(self, X):
        ''' Implement forward pass here

            Arguments
            ---------
            X: features batch

        '''
        #### Implement the forward pass here ####
        ### Forward pass ###
        # COMPLETED: Hidden layer - Replace these values with your calculations.
        hidden_inputs = np.dot(X, self.weights_input_to_hidden) # signals into hidden layer
        hidden_outputs = self.activation_function(hidden_inputs) # signals from hidden layer
        # print('hidden_inputs {} \n'.format(hidden_inputs))
        # print('hidden_outputs {} \n'.format(hidden_outputs))

        # COMPLETED: Output layer - Replace these values with your calculations.
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output) # signals into final output layer
        # final_outputs = self.activation_function(final_inputs)
        final_outputs = final_inputs # signals from final output layer
        # print('final_inputs {} \n'.format(final_inputs))
        # print('final_outputs {} \n'.format(final_outputs))

        return final_outputs, hidden_outputs

    def backpropagation(self, final_outputs, hidden_outputs, X, y, delta_weights_i_h, delta_weights_h_o):
        ''' Implement backpropagation

            Arguments
            ---------
            final_outputs: output from forward pass
            y: target (i.e. label) batch
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers

        '''
        #### Implement the backward pass here ####
        ### Backward pass ###

        # COMPLETED: Output error - Replace this value with your calculations.
        # output error (y - y-hat) - Lecture 2_2_12
        error = y - final_outputs # Output layer error is the difference between desired target and actual output.
        # print('error {} \n'.format(error))

        # COMPLETED: Calculate the hidden layer's contribution to the error
        hidden_error = error # np.dot(self.weights_hidden_to_output, error)
        # print('hidden_error {} \n'.format(hidden_error))

        # COMPLETED: Backpropagated error terms - Replace these values with your calculations.
        output_error_term = np.dot(self.weights_hidden_to_output, hidden_error)
        # print('output_error_term {} \n'.format(output_error_term))

        # from the lecture: output_error_term = error * output * (1 - output)
        # Note - it appears that output_error_term and hidden_error_term have been swapped vs. the lecture notes?
        # output_error_term = error * final_outputs * (1 - final_outputs)
        hidden_error_term = output_error_term * hidden_outputs * (1 - hidden_outputs)
        # print('hidden_error_term {} \n'.format(hidden_error_term))

        # Weight step (input to hidden)
        delta_weights_i_h += hidden_error_term * X[:, None]
        # print('Weight step: delta_weights_i_h {} \n'.format(delta_weights_i_h))

        # Weight step (hidden to output)
        delta_weights_h_o += hidden_error * hidden_outputs[:, None]
        # print('Weight step: delta_weights_h_o {} \n'.format(delta_weights_h_o))

        return delta_weights_i_h, delta_weights_h_o

    def update_weights(self, delta_weights_i_h, delta_weights_h_o, n_records):
        ''' Update weights on gradient descent step

            Arguments
            ---------
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers
            n_records: number of records

        '''
        self.weights_hidden_to_output += self.lr * delta_weights_h_o / n_records # update hidden-to-output weights with gradient descent step
        self.weights_input_to_hidden += self.lr * delta_weights_i_h / n_records # update input-to-hidden weights with gradient descent step

    def run(self, features):
        ''' Run a forward pass through the network with input features

            Arguments
            ---------
            features: 1D array of feature values
        '''

        #### Implement the forward pass here ####

        # COMPLETED: Hidden layer - replace these values with the appropriate calculations.
        ## Nearly identical to def forward_pass_train  -  features for X
        hidden_inputs = np.dot(features, self.weights_input_to_hidden) # signals into hidden layer
        hidden_outputs = self.activation_function(hidden_inputs) # signals from hidden layer

        # COMPLETED: Output layer - Replace these values with the appropriate calculations.
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output) # signals into final output layer
        final_outputs = final_inputs # signals from final output layer

        return final_outputs


#########################################################
# Set your hyperparameters here
##########################################################
iterations = 6500      # 2500, 5000, 7500, 10000
learning_rate = 0.75   # 0.1, 0.5, 1.0, 1.1
hidden_nodes = 15
output_nodes = 1
