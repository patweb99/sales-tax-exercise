import pprint
from ObjectPool import MetadataDictObjectPool

class Calculator ( object ):
    """
    The calculator worked with complex descriptions to figure out the count of items it should calculate, which items/taxable,
     and cost via single inputs. It also can take in count, the item/taxable, and cost as separate arguments via a separate
     def
    """

    def __init__(self, metadata_object_pool=None, sales_tax_percent_rate=float( 0.10 ), import_duty_sales_tax_percent_rate=float( 0.05 ), nearest_cent= 1 / 0.05 ):

        # VALIDATION
        # check to see if the object pool passed is a product object pool
        if not isinstance( metadata_object_pool, MetadataDictObjectPool ):
            raise Exception( "Metadata object pool argument is not of type MetadataDictObjectPool" )

        # check to make sure the sales tax is a float
        if not isinstance( sales_tax_percent_rate, float ):
            raise Exception( "Sales tax argument is not of type Float" )

        # check to make sure the import duty sales tax is a float
        if not isinstance( import_duty_sales_tax_percent_rate, float ):
            raise Exception( "Import duty sales tax argument is not of type Float" )

        self.metadata_object_pool = metadata_object_pool
        self.applicable_sales_tax_percent_rate = sales_tax_percent_rate
        self.applicable_import_duty_sales_tax_percent_rate = import_duty_sales_tax_percent_rate
        self.nearest_cent = nearest_cent

        self.inputted_list = []

    def input_by_full_desc( self, full_desc ):
        """
        Input the item you wish to calculate

        :param desc: Takes in the full description of a given item.
        Example: 1 book at 12.49
        :return: returns a desc object that includes all details including metadata
        """
        # extract purchase item details
        count, desc, price = self.__extract_full_desc_details( full_desc )

        # after desc data has been extracted we send it to the simpler version of input to handle the rest of the process
        return self.input( count, desc, price )

    def input( self, count, desc, price ):
        """
        Inputs the count, desc, and price of an input item

        :param count: Count of item sent in
        :param desc: Description of item sent in
        :param price: Price of item sent in
        :return: returns a desc object that includes all details including metadata
        """

        # get the metadata object based on desc
        desc_metadata_object = self.metadata_object_pool.get( desc )

        # get the sales tax
        sales_tax = self.__round_tax( self.__calculate_sales_tax( count, desc, price ) )

        # get the internaltional tax
        import_tax = self.__round_tax( self.__calculate_import_tax( count, desc, price ) )

        # create a desc object with metadata
        desc_object_with_metadata = {
            "desc_hash" : hash( desc ),
            "input_desc" : desc,
            "output_desc" : desc_metadata_object['desc'] if desc_metadata_object is not None else desc,
            "count" : count,
            "sales_tax": float( format( sales_tax, ".2f" ) ),
            "import_tax": float( format( import_tax, ".2f" ) ),
            "base_price" : float( format( price, ".2f" ) ),
            "total_price" : float( format( price + sales_tax + import_tax , ".2f" ) )
        }

        # append the item to the inputted list for later processing
        self.inputted_list.append(desc_object_with_metadata  )

        # return the details
        return desc_object_with_metadata

    def __extract_full_desc_details( self, full_desc ):
        """
        Extracts the details of the full description passed such as count, desc, and price
        This has been generally set as a private function since it really should not be used outside of the class

        :param full_desc: Full description of item (count, desc, price)
        Example: 1 book at 12.49
        :return:
        """

        # split the full desc into a string array
        purchase_arr = [x.encode('UTF8') for x in full_desc.split(' ')]

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

        # join the remaining to from the desc
        desc = str(' '.join( purchase_arr )).lower()

        return count, desc, price

    def __calculate_sales_tax( self, count, desc, price ):
        """
        Used to calculate the sales tax

        :param count: Count of item sent in
        :param desc: Description of item sent in
        :param price: Price of item sent in
        :return: Sales tax to add
        """

        # get the desc metadata object
        desc_metadata_object = self.metadata_object_pool.get( desc )
        # check to see if the desc is within
        if desc_metadata_object is not None and desc_metadata_object['is_taxable'] == True:
            return ( price * self.applicable_sales_tax_percent_rate ) * int( count )
        return 0

    def __calculate_import_tax( self, count, desc, price ):
        """
        Used to calculate the import tax

        :param count: Count of item sent in
        :param desc: Description of item sent in
        :param price: Price of item sent in
        :return: Sales tax to add
        """

        # get the desc metadata object
        desc_metadata_object = self.metadata_object_pool.get( desc )
        # check to see if the desc is within
        if desc_metadata_object is not None and desc_metadata_object['is_import'] == True:
            return ( price * self.applicable_import_duty_sales_tax_percent_rate ) * int( count )
        return 0

    def __round_tax( self, amount ):
        """
        Rounds the tax to 0.05

        :param amount: Amount to round
        :return: Rounded amount
        """

        import math
        return ( math.ceil( amount * self.nearest_cent ) / self.nearest_cent )

    def checkout( self ):
        """
        Returns a checkout summary of the items inputted into the calculator

        :return: List of checkout items based on what was inputted into the calculator. Included taxes, etc
        """

        # return checkout
        return self.inputted_list

    def checkout_sales_tax_total( self ):
        """
        Returns the summed sales taxes for checkout items

        :return: Sum of sales taxes
        """

        # get checkout information
        checkout = self.checkout()

        # sum sales taxes
        total = 0

        for item in checkout:
            total = total + item['sales_tax']

        # return total
        return float( format( total, '.2f' ) )

    def checkout_import_tax_total( self ):
        """
        Returns the summed import taxes for checkout items

        :return: Sum of import taxes
        """

        # get checkout information
        checkout = self.checkout()

        # sum import taxes
        total = 0
        for item in checkout:
            total = total + item['import_tax']

        # return total
        return float( format( total, '.2f' ) )

    def checkout_total( self ):
        """
        Returns the summed total for checkout items

        :return: Sum of total
        """

        # get checkout information
        checkout = self.checkout()

        # sum checkout total
        total = 0
        for item in checkout:
            total = total + item['total_price']

        # return total
        return float( format( total, '.2f' ) )