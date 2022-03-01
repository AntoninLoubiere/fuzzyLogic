from matplotlib.pyplot import *

from fuzzy_controller import FuzzyController

TEMP_NB_VALUES = 250


def get_values(controller, luminosity_value=40_000):
    temp_step = 30 / (TEMP_NB_VALUES - 1)
    x = []
    y = []

    for i in range(TEMP_NB_VALUES):
        x.append(t := temp_step * i)
        y.append(controller.resolve({'temperature': t, 'luminosity': luminosity_value})['store_height'])

    return x, y


def draw_temp():
    controller = FuzzyController.load_from_file('./fuzzy_controller.fzc')
    fig, ax = subplots()
    subplots_adjust(bottom=0.2)
    ax.margins(x=0)

    l, = plot(*get_values(controller))

    ax_luminosity = axes([0.25, 0.1, 0.65, 0.03])
    s_luminosity = Slider(ax_luminosity, 'Luminosity', 0, 100_000, 40_000)

    def update(val):
        l.set_ydata(get_values(controller, luminosity_value=int(val))[1])

    s_luminosity.on_changed(update)

    show()


if __name__ == '__main__':
    draw_temp()
