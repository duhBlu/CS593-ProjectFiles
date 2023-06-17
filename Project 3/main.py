import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def linear_hypothesis(x, a, b):
    return a*x + b

def cost_function(X, Y, a, b):
    return np.mean((Y - linear_hypothesis(X, a, b)) ** 2)

def gradients(X, Y, a, b):
    da = -2 * np.mean((Y - linear_hypothesis(X, a, b)) * X)
    db = -2 * np.mean(Y - linear_hypothesis(X, a, b))
    return da, db

def gradient_descent(X, Y, a, b, learning_rate, epochs, ax, fig):
    cost_history = []
    for epoch in range(epochs):
        da, db = gradients(X, Y, a, b)
        a -= learning_rate * da
        b -= learning_rate * db
        cost_history.append(cost_function(X, Y, a, b))

        # Clear previous points
        ax.clear()

        # Plot points
        ax.scatter(X, Y)

        # Plot the line
        x_values_line = np.linspace(min(X), max(X), 100)
        y_values_line = linear_hypothesis(x_values_line, a, b)
        ax.plot(x_values_line, y_values_line, 'r')

        # Set the x and y limits to include all data points
        ax.set_xlim([min(X), max(X)])
        ax.set_ylim([min(Y), max(Y)])

        # Redraw the canvas
        fig.canvas.draw()

        # Pause
        plt.pause(0.1)

    return a, b, cost_history

def stochastic_gradient_descent(X, Y, a, b, learning_rate, epochs):
    # SGD optimization
    cost_history = []
    for epoch in range(epochs):
        for i in range(len(X)):
            da, db = gradients(X[i:i+1], Y[i:i+1], a, b)
            a -= learning_rate * da
            b -= learning_rate * db
        cost_history.append(cost_function(X, Y, a, b))
    return a, b, cost_history


def main():
    
    # Create a figure and axes
    fig, ax = plt.subplots()

    # Turn on interactive mode
    plt.ion()


    # initialize lists to store x and y values
    x_values = []
    y_values = []

    with open('Project 3/Part1_x_y_Values.txt', 'r') as f:
        lines = f.readlines()

        for line in lines[1:]:
            # Remove parentheses and split string at comma
            x, y = line.strip()[1:-1].split(', ')
            x = x.replace(',','')
            y = y.replace(',','')
            # Append values to respective lists
            x_values.append(float(x))
            y_values.append(float(y))

    for i in range(len(x_values)):
        # Clear previous points
        ax.clear()

        # Plot points
        ax.scatter(x_values[:i+1], y_values[:i+1])

        x_min = min(x_values) - 5
        x_max = max(x_values) + 5
        y_min = min(y_values) - 5
        y_max = max(y_values) + 5
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        # Redraw the canvas
        fig.canvas.draw()


    
    X = np.array(x_values)
    Y = np.array(y_values)

    # Initialize parameters
    a, b = 0.0, 0.0
    learning_rate = 0.01
    epochs = 100

    # Run GD
    a_gd, b_gd, cost_history_gd = gradient_descent(X, Y, a, b, learning_rate, epochs, ax, fig)

    # Turn off interactive mode
    plt.ioff()

    # Keep the window open once all points have been drawn
    plt.show()


if __name__ == "__main__":
    main()