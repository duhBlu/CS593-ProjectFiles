import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


'''
Functions to handle 3 features
'''
def quadratic_hypothesis(x, a, b, c):
    return a * (x ** 2) + b * x + c

def cost_function(X, Y, a, b, c):
    return np.mean((Y - quadratic_hypothesis(X, a, b, c)) ** 2)

'''
Gradient Descent functions
'''
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
        
        ax.plot(x_values_line, y_values_line, 'r', label='Epoch: {}'.format(epoch))
        
        ax.legend()
        ax.set_title("Gradient Descent")
        
        ax.set_xlim([min(X), max(X)])
        ax.set_ylim([min(Y), max(Y)])
        fig.canvas.draw()
        
        plt.pause(0.01)
    return a, b, c, cost_history

'''
Stochastic Gradient Descent functions
'''
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
        ax.plot(x_values_line, y_values_line, 'r', label='Epoch: {}'.format(epoch))
        
        ax.legend()
        ax.set_title("Stochastic Descent")

        ax.set_xlim([min(X), max(X)])
        ax.set_ylim([min(Y), max(Y)])
        fig.canvas.draw()
        plt.pause(0.01)

    return a, b, c, cost_history
'''
Mini Batch Stochastic Gradient Descent functions
'''
def mini_batch_gradients(X, Y, a, b, c, batch_size):
    indices = np.random.choice(len(X), batch_size)
    X_batch = X[indices]
    Y_batch = Y[indices]
    da = -2 * np.mean((Y_batch - quadratic_hypothesis(X_batch, a, b, c)) * X_batch ** 2)
    db = -2 * np.mean((Y_batch - quadratic_hypothesis(X_batch, a, b, c)) * X_batch)
    dc = -2 * np.mean(Y_batch - quadratic_hypothesis(X_batch, a, b, c))
    return da, db, dc

def mini_batch_gradient_descent(X, Y, a, b, c, learning_rate, epochs, batch_size, ax, fig):
    cost_history = []
    for epoch in range(epochs):
        da, db, dc = mini_batch_gradients(X, Y, a, b, c, batch_size)
        a -= learning_rate * da
        b -= learning_rate * db
        c -= learning_rate * dc
        cost_history.append(cost_function(X, Y, a, b, c))

        ax.clear()
        ax.scatter(X, Y)

        x_values_line = np.linspace(min(X), max(X), 100)
        y_values_line = quadratic_hypothesis(x_values_line, a, b, c)
        ax.plot(x_values_line, y_values_line, 'r', label='Epoch: {}'.format(epoch))
        
        ax.legend()
        ax.set_title("Mini-Batch Descent")

        ax.set_xlim([min(X), max(X)])
        ax.set_ylim([min(Y), max(Y)])
        fig.canvas.draw()
        plt.pause(0.01)

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
    learning_rate = 0.001
    epochs = 100
    
    plt.pause(5)
    
    # Run Gradient Descent
    a_gd, b_gd, c_gd, cost_history_gd = gradient_descent(X, Y, a, b, c, learning_rate, epochs, ax, fig)
    print(str(a_gd) + "\n" + str(b_gd) + "\n" + str(c_gd) + "\n" + str(cost_history_gd))

    # Clear ax before running SGD
    ax.clear()

    # Run Stochastic Gradient Descent
    a_sgd, b_sgd, c_sgd, cost_history_sgd = stochastic_gradient_descent(X, Y, a, b, c, learning_rate, epochs, ax, fig)
    print(str(a_sgd) + "\n" + str(b_sgd) + "\n" + str(c_sgd) + "\n" + str(cost_history_sgd))
    
    # Clear ax before running mini_batch SGD
    ax.clear()

    # Run Mini-batch Gradient Descent
    batch_size = 32  # You can adjust this value
    a_mbgd, b_mbgd, c_mbgd, cost_history_mbgd = mini_batch_gradient_descent(X, Y, a, b, c, learning_rate, epochs, batch_size, ax, fig)
    print(str(a_mbgd) + "\n" + str(b_mbgd) + "\n" + str(c_mbgd) + "\n" + str(cost_history_mbgd))



    # Clear ax before plotting cost history
    ax.clear()
    
    
    # Create a figure with 3 subplots
    fig, axs = plt.subplots(3, figsize=(10,15))

    # Plot cost history for each gradient descent method in a different subplot
    axs[0].plot(cost_history_gd, label="Gradient Descent")
    axs[0].set_title("Cost History (Gradient Descent)")
    axs[0].set_xlabel("Epoch")
    axs[0].set_ylabel("Cost")
    axs[0].legend()

    axs[1].plot(cost_history_sgd, label="Stochastic Gradient Descent", color='orange')
    axs[1].set_title("Cost History (Stochastic Gradient Descent)")
    axs[1].set_xlabel("Epoch")
    axs[1].set_ylabel("Cost")
    axs[1].legend()

    axs[2].plot(cost_history_mbgd, label="Mini-batch Gradient Descent", color='green')
    axs[2].set_title("Cost History (Mini-batch Gradient Descent)")
    axs[2].set_xlabel("Epoch")
    axs[2].set_ylabel("Cost")
    axs[2].legend()

    # Adjust the layout so the plots do not overlap
    fig.tight_layout()

    # Turn off interactive mode
    plt.ioff()

    # Keep the window open once all points have been drawn
    plt.show()

if __name__ == "__main__":
    main()
