import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
import matplotlib.animation as animation

class Charts:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = None
        self.plots = []

    def plot_surface_chart(self, data):
        x_axis = np.arange(0, len(data), 1)
        y_axis = np.arange(0, len(data[0]), 1)
        x_axis, y_axis = np.meshgrid(x_axis, y_axis)
        z_axis = np.array(data)
        z_axis = np.transpose(z_axis)
        self.plots.append(self.ax.plot_surface(x_axis, y_axis, z_axis, cmap=cm.coolwarm))

    def redraw(self):
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def prepare(self, chart_no):
        self.ax = self.fig.add_subplot(projection='3d')

    def update_plot(self, frame_number, zarray, plot):
        plot[0].remove()
        plot[0] = self.ax.plot_surface(x, y, self.plots[frame_number], cmap="magma")

    def set_title_labels(self, title, x_label, y_label, z_label):
        plt.title(title)
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.ax.set_zlabel(z_label)


    def show(self):
        #nmax = 20
        #animate = animation.FuncAnimation(self.fig, self.update_plot, nmax, fargs=(self.plots, plot))
        plt.show()

    def plot_polar_chart(self):
        return 0

    def plot_scatter_chart(self):
        return 0

    def clear_charts(self):
        plt.cla()
        plt.clf()
        plt.close()
        self.plots.clear()
