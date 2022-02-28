from fuzzy_controller import FuzzyController
from fuzzy_sets.linear_fuzzy_set_helpers import left_trapeze_set, trapeze_set, right_trapeze_set
from rules.fuzzy_expression import fe_name
from rules.rules import FuzzyRule
from rules.values import LinguisticValue
from rules.variables import LinguisticVariable
from matplotlib.pyplot import *

TEMP_NB_VALUES = 250


def create_controller():
    temperature = LinguisticVariable("temperature", [
        LinguisticValue("cold", left_trapeze_set(0, 30, 10, 12)),
        LinguisticValue("fresh", trapeze_set(0, 30, 10, 12, 15, 17)),
        LinguisticValue("good", trapeze_set(0, 30, 13, 17, 20, 25)),
        LinguisticValue("hot", right_trapeze_set(0, 30, 20, 28))
    ])
    luminosity = LinguisticVariable("luminosity", [
        LinguisticValue("dark", left_trapeze_set(0, 100_000, 20_000, 30_000)),
        LinguisticValue("medium", trapeze_set(0, 100_000, 20_000, 30_000, 60_000, 85_000)),
        LinguisticValue("light", right_trapeze_set(0, 100_000, 60_000, 85_000))
    ])
    store_height = LinguisticVariable("store_height", [
        LinguisticValue("down", left_trapeze_set(0, 105, 25, 40)),
        LinguisticValue("medium", trapeze_set(0, 105, 25, 40, 85, 100)),
        LinguisticValue("up", right_trapeze_set(0, 105, 85, 100))
    ])
    controller = FuzzyController([temperature, luminosity, store_height], [
        FuzzyRule(
            [fe_name(temperature, 'cold')], [fe_name(store_height, 'up')]
        ),
        FuzzyRule(
            [fe_name(temperature, 'fresh'), fe_name(luminosity, 'dark')], [fe_name(store_height, 'up')]
        ),
        FuzzyRule(
            [fe_name(temperature, 'fresh'), fe_name(luminosity, 'medium')], [fe_name(store_height, 'up')]
        ),
        FuzzyRule(
            [fe_name(temperature, 'fresh'), fe_name(luminosity, 'light')], [fe_name(store_height, 'medium')]
        ),
        FuzzyRule(
            [fe_name(temperature, 'good'), fe_name(luminosity, 'dark')], [fe_name(store_height, 'up')]
        ),
        FuzzyRule(
            [fe_name(temperature, 'good'), fe_name(luminosity, 'medium')], [fe_name(store_height, 'medium')]
        ),
        FuzzyRule(
            [fe_name(temperature, 'good'), fe_name(luminosity, 'light')], [fe_name(store_height, 'medium')]
        ),
        FuzzyRule(
            [fe_name(temperature, 'hot')], [fe_name(store_height, 'down')]
        )
    ])
    return controller


def get_values(controller, luminosity_value=40_000):
    temp_step = 30 / (TEMP_NB_VALUES - 1)
    x = []
    y = []

    for i in range(TEMP_NB_VALUES):
        x.append(t := temp_step * i)
        y.append(controller.resolve({'temperature': t, 'luminosity': luminosity_value})['store_height'])

    return x, y


def draw_temp():
    controller = create_controller()
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
