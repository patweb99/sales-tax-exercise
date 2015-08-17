from nose.tools import assert_not_equals, assert_equals
from lettuce import *

@step(u'Given that an item with description "([^"]*)", is_taxable "([^"]*)", is_import "([^"]*)" is added to the object pool')
def given_that_an_item_with_description_is_taxable_is_import_is_added_to_the_object_pool( step, desc, is_taxable, is_import ):
    # create object witin pool
    world.empty_object_pool.add(
        desc=desc,
        is_taxable=is_taxable,
        is_import=is_import
    )
    assert True

@step(u'Then there should be an item with description "([^"]*)", is_taxable "([^"]*)", is_import "([^"]*)" within the object pool')
def then_there_should_be_an_item_with_description_is_taxable_is_import_within_the_object_pool( step, desc, is_taxable, is_import ):
    # get object from pool
    obj = world.empty_object_pool.get( desc )

    # check to make sure the object is not none and has defs
    assert_not_equals( None, obj )
    assert_equals( obj['desc'], desc )
    assert_equals( obj['alias_arr'], None )
    assert_equals( obj['is_taxable'], is_taxable )
    assert_equals( obj['is_import'], is_import )

@step(u'Given that an item with description "([^"]*)", alias_arr "([^"]*)", is_taxable "([^"]*)", is_import "([^"]*)" is added to the object pool')
def given_that_an_item_with_description_is_taxable_alias_arr_is_import_is_added_to_the_object_pool( step, desc, alias_arr, is_taxable, is_import ):
    # create object witin pool
    world.empty_object_pool.add(
        desc=desc,
        alias_arr=alias_arr,
        is_taxable=is_taxable,
        is_import=is_import
    )
    assert True

@step(u'Then there should be an item with description "([^"]*)", alias_arr "([^"]*)", is_taxable "([^"]*)", is_import "([^"]*)" within the object pool')
def then_there_should_be_an_item_with_description_alias_arr_is_taxable_is_import_within_the_object_pool( step, desc, alias_arr, is_taxable, is_import ):
    # get object from pool
    obj = world.empty_object_pool.get( desc )

    # check to make sure the object is not none and has defs
    assert_not_equals( None, obj )
    assert_equals( obj['desc'], desc )
    assert_equals( obj['alias_arr'], alias_arr )
    assert_equals( obj['is_taxable'], is_taxable )
    assert_equals( obj['is_import'], is_import )

