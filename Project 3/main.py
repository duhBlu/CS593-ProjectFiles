import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def quadratic_hypothesis(x, a, b, c):
    return a * (x ** 2) + b * x + c

def cost_function(X, Y, a, b, c):
    return np.mean((Y - quadratic_hypothesis(X, a, b, c)) ** 2)

def gradients(X, Y, a, b, c):
    da = -2 * np.mean((Y - quadratic_hypothesis(X, a, b, c)) * X ** 2)
    db = -2 * np.mean((Y - quadratic_hypothesis(X, a, b, c)) * X)
    dc = -2 * np.mean(Y - quadratic_hypothesis(X, a, b, c))
    return da, db, dc

def gradient_descent(X, Y, a, b, c, learning_rate, epochs, ax, fig):
    cost_history = []
    for epoch in range(epochs):
        da, db, dc = gradients(X, Y, a, b, c)
        a -= learning_rate * da
        b -= learning_rate * db
        c -= learning_rate * dc
        cost_history.append(cost_function(X, Y, a, b, c))

        ax.clear()

        ax.scatter(X, Y)

        x_values_line = np.linspace(min(X), max(X), 100)
        y_values_line = quadratic_hypothesis(x_values_line, a, b, c)
        ax.plot(x_values_line, y_values_line, 'r')

        ax.set_xlim([min(X), max(X)])
        ax.set_ylim([min(Y), max(Y)])

        fig.canvas.draw()

        plt.pause(0.01)

    return a, b, c, cost_history

def stochastic_gradients(x, y, a, b, c):
    da = -2 * (y - quadratic_hypothesis(x, a, b, c)) * (x ** 2)
    db = -2 * (y - quadratic_hypothesis(x, a, b, c)) * x
    dc = -2 * (y - quadratic_hypothesis(x, a, b, c))
    return da, db, dc

def stochastic_gradient_descent(X, Y, a, b, c, learning_rate, epochs, ax, fig):
    cost_history = []
    for epoch in range(epochs):
        for i in range(len(X)):
            da, db, dc = stochastic_gradients(X[i], Y[i], a, b, c)
            a -= learning_rate * da
            b -= learning_rate * db
            c -= learning_rate * dc

        cost_history.append(cost_function(X, Y, a, b, c))

        ax.clear()
        ax.scatter(X, Y)

        x_values_line = np.linspace(min(X), max(X), 100)
        y_values_line = quadratic_hypothesis(x_values_line, a, b, c)
        ax.plot(x_values_line, y_values_line, 'r')

        ax.set_xlim([min(X), max(X)])
        ax.set_ylim([min(Y), max(Y)])

        fig.canvas.draw()
        plt.pause(0.1)

    return a, b, c, cost_history

def main():

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(10, 5))

    # Turn on interactive mode
    plt.ion()

    # Initialize lists to store x and y values
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

    X = np.array(x_values)
    Y = np.array(y_values)
    # Normalizing data
    X = (X - np.mean(X)) / np.std(X)
    Y = (Y - np.mean(Y)) / np.std(Y)
    a, b, c = 0.0, 0.0, 0.0
    learning_rate = 0.01
    epochs = 100

    # Run Gradient Descent
    a_gd, b_gd, c_gd, cost_history_gd = gradient_descent(X, Y, a, b, c, learning_rate, epochs, ax, fig)
    print(str(a_gd) + "\n" + str(b_gd) + "\n" + str(c_gd) + "\n" + str(cost_history_gd))

    # Clear ax before running SGD
    ax.clear()

    # Run Stochastic Gradient Descent
    a_sgd, b_sgd, c_sgd, cost_history_sgd = stochastic_gradient_descent(X, Y, a, b, c, learning_rate, epochs, ax, fig)
    print(str(a_sgd) + "\n" + str(b_sgd) + "\n" + str(c_sgd) + "\n" + str(cost_history_sgd))

    # Clear ax before plotting cost history
    ax.clear()

    # Plot cost history
    ax.plot(cost_history_gd, label="Gradient Descent")
    ax.plot(cost_history_sgd, label="Stochastic Gradient Descent")
    ax.set_title("Cost History")
    ax.set_xlabel("Epoch")
    ax.set_ylabel("Cost")
    ax.legend()

    # Turn off interactive mode
    plt.ioff()

    # Keep the window open once all points have been drawn
    plt.show()

if __name__ == "__main__":
    main()
