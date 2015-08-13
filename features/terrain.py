
from lettuce import *
from SalesTax import Calculator

@before.each_scenario
def setup_some_scenario(scenario):

    # create a new calculator per scenario
    world.calculator = Calculator()