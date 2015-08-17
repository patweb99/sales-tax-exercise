
from lettuce import *
from SalesTax import Calculator, MetadataDictObjectPool

@before.each_feature
def setup(feature):

    # create object pool of lookup items
    object_pool = MetadataDictObjectPool()
    object_pool.add( desc="Book", is_taxable=False, is_import=False )
    object_pool.add( desc="music CD", is_taxable=True, is_import=False )
    object_pool.add( desc="chocolate bar", is_taxable=False, is_import=False )
    object_pool.add( desc="imported box of chocolates", alias_arr=["box of imported chocolates"], is_taxable=False, is_import=True )
    object_pool.add( desc="imported bottle of perfume", is_taxable=True, is_import=True )
    object_pool.add( desc="bottle of perfume", is_taxable=True, is_import=False )
    object_pool.add( desc="packet of headache pills", is_taxable=False, is_import=False )

    world.object_pool = object_pool

@before.each_scenario
def setup_some_scenario(scenario):

    # create a new calculator per scenario
    world.calculator = Calculator( metadata_object_pool=world.object_pool )

    world.empty_object_pool = MetadataDictObjectPool()