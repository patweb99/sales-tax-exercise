Feature: Sales Calculator

    Scenario: (Non-taxable) Basic sales tax is applicable at a rate of 10% on all goods, except books, food, andmedical products that are exempt.
        Given I have a purchase item of "1 book at 12.49"
        Then I have a purchase item total price of "12.49" in the checkout list for item "book"

    Scenario: (Taxable) Basic sales tax is applicable at a rate of 10% on all goods, except books, food, andmedical products that are exempt.
        Given I have a purchase item of "1 music CD at 14.99"
        Then I have a purchase item total price of "16.49" in the checkout list for item "music CD"

    Scenario: Import duty is an additional imported goods at a rate of 5%, with no exemptions.
        Given I have a purchase item of "1 imported box of chocolates at 10.00"
        Then I have a purchase item total price of "10.50" in the checkout list for item "imported box of chocolates"

    Scenario: (Input 1) When I purchase items I receive a receipt, which lists the name of all the items and their price (including tax), finishing with the total cost of the items, and the total amounts of sales taxes paid.
        Given I have a purchase item of "1 book at 12.49"
        Given I have a purchase item of "1 music CD at 14.99"
        Given I have a purchase item of "1 chocolate bar at 0.85"
        Then I get an output of purchase item of "1 book: 12.49"
        Then I get an output of purchase item of "1 music CD: 16.49"
        Then I get an output of purchase item of "1 chocolate bar: 0.85"
        Then I get a total sales tax of "1.50"
        Then I get a total of "29.83"

    Scenario: (Input 2) When I purchase items I receive a receipt, which lists the name of all the items and their price (including tax), finishing with the total cost of the items, and the total amounts of sales taxes paid.
        Given I have a purchase item of "1 imported box of chocolates at 10.00"
        Given I have a purchase item of "1 imported bottle of perfume at 47.50"
        Then I get an output of purchase item of "1 imported box of chocolates: 10.50"
        Then I get an output of purchase item of "1 imported bottle of perfume: 54.65"
        Then I get a total sales tax of "7.65"
        Then I get a total of "65.15"

    Scenario: (Input 3) When I purchase items I receive a receipt, which lists the name of all the items and their price (including tax), finishing with the total cost of the items, and the total amounts of sales taxes paid.
        Given I have a purchase item of "1 imported bottle of perfume at 27.99"
        Given I have a purchase item of "1 bottle of perfume at 18.99"
        Given I have a purchase item of "1 packet of headache pills at 9.75"
        Given I have a purchase item of "1 box of imported chocolates at 11.25"
        Then I get an output of purchase item of "1 imported bottle of perfume: 32.19"
        Then I get an output of purchase item of "1 bottle of perfume: 20.89"
        Then I get an output of purchase item of "1 packet of headache pills: 9.75"
        Then I get an output of purchase item of "1 imported box of chocolates: 11.85"
        Then I get a total sales tax of "6.70"
        Then I get a total of "74.68"
