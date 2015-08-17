# Created by patricksantora at 8/16/15
Feature: ObjectPool MetadataDictObjectPool
  # Enter feature description here

    Scenario: Add item with alias to the object pool
        Given that an item with description "Test item", is_taxable "True", is_import "False" is added to the object pool
        Then there should be an item with description "Test item", is_taxable "True", is_import "False" within the object pool

    Scenario: Add item with alias to the object pool
        Given that an item with description "Test item", alias_arr "['1','2','3']", is_taxable "True", is_import "False" is added to the object pool
        Then there should be an item with description "Test item", alias_arr "['1','2','3']", is_taxable "True", is_import "False" within the object pool
