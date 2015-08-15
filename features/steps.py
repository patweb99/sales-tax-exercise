from nose.tools import assert_equals
from lettuce import *

@step(u'Given I have a purchase item of "([^"]*)"')
def given_i_have_a_purchase_item_of_group1(step, group1):
    world.calculator.input_by_full_desc( group1 )
    assert True

@step(u'Then I have a purchase item total price of "([^"]*)" in the checkout list for item "([^"]*)"')
def then_i_have_a_purchase_item_total_price_of_group1_in_the_checkout_list(step, group1, group2):

    # purchase item details
    checkout = world.calculator.checkout()

    # get the purchase item information
    price_in = str( group1 )
    purchase_item_in = group2.lower()

    # loop over the checkout items and find the purchase item in question
    found = False
    for item in checkout:
        if item['input_desc'] == purchase_item_in:
            found = True
            assert_equals( item['total_price'], float( price_in ) )

    assert found, "Item not found \"{0}\"".format( group1 )

@step(u'And I have a purchase item of "([^"]*)"')
def and_i_have_a_purchase_item_of_group1(step, group1):
    world.calculator.input_by_full_desc( group1 )
    assert True

@step(u'Then I get an output of purchase item of "([^"]*)"')
def then_i_get_an_output_of_purchase_item_of_group1(step, group1):
    # purchase item details
    checkout = world.calculator.checkout()

    # get the purchase item
    purchase_in = group1.lower()

    # loop over the checkout items and find the purchase item in question
    found = False
    for item in checkout:
        checkout_purchase = "{0} {1}: {2}".format( item['count'], item['output_desc'], format( item['total_price'], '.2f' ) )
        if checkout_purchase == purchase_in:
            found = True
            assert_equals( checkout_purchase, purchase_in )

    assert found, "Item not found from \"{0}\"".format( group1 )

@step(u'Then I get a total sales tax of "([^"]*)"')
def and_i_get_a_total_sales_tax_of_group1(step, group1):

    # total information
    total_in = float( group1 )

    assert_equals( world.calculator.checkout_sales_tax_total() + world.calculator.checkout_import_tax_total(), total_in )

@step(u'Then I get a total of "([^"]*)"')
def and_i_get_a_total_of_group1(step, group1):
    # total information
    total_in = float( group1 )

    assert_equals( world.calculator.checkout_total(), total_in )

@step(u'Given I have a total of "([^"]*)"')
def given_i_have_a_total_of_group1(step, group1):
    world.round_up_var = float( group1 )
    assert True

@step(u'Then I get a new price of "([^"]*)" when I round to the nearest 0.05')
def then_i_get_a_new_price_of_group1_when_i_round_the_nearest_0_05(step, group1):
    assert_equals( world.calculator._round_tax( world.round_up_var ), float( group1 ) )