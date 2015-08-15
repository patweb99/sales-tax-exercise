
class MetadataDictObjectPool( object ):
    """
    The metadata dictionary is a pool of metadata associated to items that should be taxed, marked as import, etc
    It can be optionally used within the calulator to assist with determining if the item should meet certain criteria's
    """

    metadata_dict_object_pool = {}

    def add( self, desc, alias_arr=None, is_taxable=False, is_import=False ):
        """
        Adds a metadata object to the object pool

        :param desc: Description of item
        :param alias_arr: Alias array for item
        :param is_sales_taxable: True/False if sales taxed
        :param is_import: True/False if imported
        :return:
        """
        # add/update item to dict. use hash of description as key
        self.metadata_dict_object_pool[ hash( desc.lower() ) ] = {
            'desc': desc.lower(),
            'alias_arr' : alias_arr,
            'is_taxable': is_taxable,
            'is_import': is_import
        }

    def get( self, desc ):
        """
        Looks up and returns the given metadata object from the OBJECT POOL ITEMS collection

        :param desc: Description/Alias of item that you'd like to get from the object pool
        :return: Item matching description or None if item is not found
        """

        # look over object pool and check to see if the object is within the pool
        if hash( desc ) in self.metadata_dict_object_pool.keys():
            return self.metadata_dict_object_pool[ hash( desc ) ]

        # look for aliases
        for item in self.metadata_dict_object_pool.values():
            if item['alias_arr'] is not None and desc in item['alias_arr']:
                return item

        # return none if item is not found
        return None