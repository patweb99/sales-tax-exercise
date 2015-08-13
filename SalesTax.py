
class Calculator ( object ):

    # constants
    APPLICABLE_SALES_TAX_PERCENT_RATE = float( 0.10 )
    APPLICABLE_IMPORT_DUTY_SALES_TAX_PERCENT_RATE = float( 0.05 )
    NEAREST_CENT = 1 / 0.05

    def __init__(self, preload=True):
        self.REFERENCE_ITEMS_STORE = {}
        self.SHOPPING_LIST = []

        # preload some data to refer against
        if preload:
            self.add_reference( desc="Book", is_taxable=False, is_import=False )
            self.add_reference( desc="music CD", is_taxable=True, is_import=False )
            self.add_reference( desc="chocolate bar", is_taxable=False, is_import=False )
            self.add_reference( desc="imported box of chocolates", alias="box of imported chocolates", is_taxable=False, is_import=True )
            self.add_reference( desc="imported bottle of perfume", is_taxable=True, is_import=True )
            self.add_reference( desc="bottle of perfume", is_taxable=True, is_import=False )
            self.add_reference( desc="packet of headache pills", is_taxable=False, is_import=False )

    def add_reference( self, desc, is_taxable=False, is_import=False, alias=None ):
        # add/update item to dict. use hash of description as key
        self.REFERENCE_ITEMS_STORE[ self._create_purchase_item_hash( desc.lower() ) ] = {
            'desc': desc.lower(),
            'alias' : alias,
            'is_taxable': is_taxable,
            'is_import': is_import
        }

        # if an alias is needed then go ahead and create a record for the alias, but keep the same description as above
        if alias:
            self.REFERENCE_ITEMS_STORE[ self._create_purchase_item_hash( alias.lower() ) ] = {
                'desc': desc.lower(),
                'alias' : alias,
                'is_taxable': is_taxable,
                'is_import': is_import
            }

    def add_purchase_item( self, purchase_item ):
        # extract purchase item details
        purchase_item_details = self.extract_purchase_item_details( purchase_item )
        # parse the purchase to get the details and add it to the shopping list
        self.SHOPPING_LIST.append( purchase_item_details )

    def extract_purchase_item_details( self, purchase_item ):

        # split the purchase into a string array
        purchase_arr = [x.encode('UTF8') for x in purchase_item.split(' ')]

        # pull out the count purchased (position 0)
        try:
            count = purchase_arr.pop(0)
        except Exception, e:
            raise Exception( "Either there is no purchase count or it's not a number" )

        # pull out the sale price of purchase
        try:
            price = float( purchase_arr.pop( len( purchase_arr ) - 1 ) )
        except Exception, e:
            raise Exception( "Either there is no purchase price or it's not a float" )

        # only strip out "at" if it exists
        if purchase_arr[-1:][0] == 'at':
            # pop out the "at"
            purchase_arr.pop( len( purchase_arr ) - 1 )

        # join the remaining to form the purchase item
        purchase_item = str(' '.join( purchase_arr )).lower()
        purchase_item_hash = self._create_purchase_item_hash( purchase_item )

        # return the details
        return {
            "reference_key" : purchase_item_hash,
            "reference" : self.REFERENCE_ITEMS_STORE[ purchase_item_hash ],
            "count" : count,
            "purchase_item" : purchase_item,
            "price" : price
        }

    def _create_purchase_item_hash( self, product_item ):
        return hash( product_item )

    def _calculate_sales_tax( self, purchase_item, count, price ):
        purchase_item_hash = self._create_purchase_item_hash( purchase_item )
        if purchase_item_hash in self.REFERENCE_ITEMS_STORE and self.REFERENCE_ITEMS_STORE[purchase_item_hash]['is_taxable'] == True:
            return ( price * self.APPLICABLE_SALES_TAX_PERCENT_RATE ) * int( count )
        return 0

    def _calculate_import_tax( self, purchase_item, count, price ):
        purchase_item_hash = self._create_purchase_item_hash( purchase_item )
        if purchase_item_hash in self.REFERENCE_ITEMS_STORE and self.REFERENCE_ITEMS_STORE[purchase_item_hash]['is_import'] == True:
            return ( price * self.APPLICABLE_IMPORT_DUTY_SALES_TAX_PERCENT_RATE ) * int( count )
        return 0

    def _round_tax( self, price ):
        import math
        return ( math.ceil( price * self.NEAREST_CENT ) / self.NEAREST_CENT )

    def checkout( self ):

        # holds the checkout items
        checkout_list = []

        # loop over the shopping list
        for item in self.SHOPPING_LIST:

            # simplify the variables
            count = item['count']
            purchase_item = item['reference']['desc']
            price = item['price']
            item_total = price

            # get the sales tax
            sales_tax = self._round_tax( self._calculate_sales_tax( purchase_item, count, price ) )
            item_total = item_total + sales_tax

            # get the internaltional tax
            import_tax = self._round_tax( self._calculate_import_tax( purchase_item, count, price ) )
            item_total = item_total + import_tax

            # add in the checkout item
            checkout_list.append({
                "count" : count,
                "purchase_item" : purchase_item,
                "price" : float( format( price, '.2f') ),
                "sales_tax" : float( format( sales_tax, '.2f') ),
                "import_tax" : float( format( import_tax, '.2f') ),
                "total": float( format( item_total, '.2f' ) )
            })

        # return checkout
        return checkout_list

    def checkout_sales_tax_total( self ):

        checkout = self.checkout()

        total = 0
        for item in checkout:
            total = total + item['sales_tax']
            total = total + item['import_tax']

        return float( format( total, '.2f' ) )

    def checkout_total( self ):

        checkout = self.checkout()

        total = 0
        for item in checkout:
            total = total + item['total']

        return float( format( total, '.2f' ) )