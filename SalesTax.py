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
        desc = str(' '.join( purchase_arr ))

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

if __name__ == "__main__":

    # create object pool of lookup items
    object_pool = MetadataDictObjectPool()
    object_pool.add( desc="Book", is_taxable=False, is_import=False )
    object_pool.add( desc="music CD", is_taxable=True, is_import=False )
    object_pool.add( desc="chocolate bar", is_taxable=False, is_import=False )
    object_pool.add( desc="imported box of chocolates", alias_arr=["box of imported chocolates"], is_taxable=False, is_import=True )
    object_pool.add( desc="imported bottle of perfume", is_taxable=True, is_import=True )
    object_pool.add( desc="bottle of perfume", is_taxable=True, is_import=False )
    object_pool.add( desc="packet of headache pills", is_taxable=False, is_import=False )

    #######################################
    # INPUT 1 (USED FOR PRINTOUT)
    #######################################
    # placing in tabs to support output
    input = """
    \tInput 1:
    \t1 Book at 12.49
    \t1 music CD at 14.99
    \t1 chocolate bar at 0.85
    """

    """
    Output 1:
    1 Book: 12.49
    1 music CD: 16.49
    1 chocolate bar: 0.85
    Sales Taxes: 1.50
    Total: 29.83
    """
    # create calculator object and inject the metadata pool
    calculator = Calculator( metadata_object_pool=object_pool )

    # input the items
    # we do half with a full description
    # we do the other half with a broken down description
    calculator.input_by_full_desc( full_desc="1 Book at 12.49" )
    calculator.input_by_full_desc( full_desc="1 music CD at 14.99" )
    calculator.input_by_full_desc( full_desc="1 chocolate bar at 0.85" )

    # checkout items
    checkout = calculator.checkout()
    # total sales tax
    total_sales_tax = calculator.checkout_sales_tax_total()
    # total import tax
    total_import_tax = calculator.checkout_import_tax_total()
    # total price
    total = calculator.checkout_total()

    print input
    # print out the checkout
    # print out each item, then sales tax, then import tax
    print "\tOutput 1:"
    for item in checkout:
        print "\t{0} {1}: {2}".format( item['count'], item['output_desc'], format( item['total_price'], '.2f' ) )
    print "\tSales Taxes: {0}".format( format( total_sales_tax + total_import_tax, ".2f" ) )
    print "\tTotal: {0}".format( format( total, ".2f" ) )

    #######################################
    # INPUT 2 (USED FOR PRINTOUT)
    #######################################
    # placing in tabs to support output
    input = """
    \tInput 2:
    \t1 imported box of chocolates at 10.00
    \t1 imported bottle of perfume at 47.50
    """

    """
    Output 2:
    1 imported box of chocolates: 10.50
    1 imported bottle of perfume: 54.65
    Sales Taxes: 7.65
    Total: 65.15
    """
    # create calculator object and inject the metadata pool
    calculator = Calculator( metadata_object_pool=object_pool )

    # input the items
    # we do half with a full description
    # we do the other half with a broken down description
    calculator.input( count=1, desc="imported box of chocolates", price=10.00 )
    calculator.input( count=1, desc="imported bottle of perfume", price=47.50 )

    # checkout items
    checkout = calculator.checkout()
    # total sales tax
    total_sales_tax = calculator.checkout_sales_tax_total()
    # total import tax
    total_import_tax = calculator.checkout_import_tax_total()
    # total price
    total = calculator.checkout_total()

    print input
    # print out the checkout
    # print out each item, then sales tax, then import tax
    print "\tOutput 2:"
    for item in checkout:
        print "\t{0} {1}: {2}".format( item['count'], item['output_desc'], format( item['total_price'], '.2f' ) )
    print "\tSales Taxes: {0}".format( format( total_sales_tax + total_import_tax, ".2f" ) )
    print "\tTotal: {0}".format( format( total, ".2f" ) )

    #######################################
    # INPUT 3 (USED FOR PRINTOUT)
    #######################################
    # placing in tabs to support output
    input = """
    \tInput 3:
    \t1 imported bottle of perfume at 27.99
    \t1 bottle of perfume at 18.99
    \t1 packet of headache pills at 9.75
    \t1 box of imported chocolates at 11.25
    """
    """
    Output 3:
    1 imported bottle of perfume: 32.19
    1 bottle of perfume: 20.89
    1 packet of headache pills: 9.75
    1 imported box of chocolates: 11.85
    Sales Taxes: 6.70
    Total: 74.68
    """
    # create calculator object and inject the metadata pool
    calculator = Calculator( metadata_object_pool=object_pool )

    # input the items
    # we do half with a full description
    # we do the other half with a broken down description
    calculator.input_by_full_desc( full_desc="1 imported bottle of perfume at 27.99" )
    calculator.input_by_full_desc( full_desc="1 bottle of perfume at 18.99" )
    calculator.input( count=1, desc="packet of headache pills", price=9.75 )
    calculator.input( count=1, desc="box of imported chocolates", price=11.25 )

    # checkout items
    checkout = calculator.checkout()
    # total sales tax
    total_sales_tax = calculator.checkout_sales_tax_total()
    # total import tax
    total_import_tax = calculator.checkout_import_tax_total()
    # total price
    total = calculator.checkout_total()

    print input
    # print out the checkout
    # print out each item, then sales tax, then import tax
    print "\tOutput 3:"
    for item in checkout:
        print "\t{0} {1}: {2}".format( item['count'], item['output_desc'], format( item['total_price'], ".2f" ) )
    print "\tSales Taxes: {0}".format( format( total_sales_tax + total_import_tax, ".2f" ) )
    print "\tTotal: {0}".format( format( total, ".2f" ) )
