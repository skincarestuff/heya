import numpy as np
import macros

# # # # # # # # #
# ALGORITHM SETUP
# # # # # # # # #

# client information 
#  produce a static structure called "client"
""" import and configure relevant client's survey data. client should contain:
      client.age (int)
      client.sex (int, 0 for female and 1 for male)
      client.race (list of strings)
      client.conds (list of ints, 0 for not diagnosed and 1 for diagnosed
         -compare list of ints to list of conditions: macros.CONDITIONS
      client.sliders (list of ints which correspond to slider values)
         -compare list of ints to list of sliders: macros.SLIDERS
      client.preferences (list of ints, on 0-1 scales or 0-2 scales depending on 
        preference. Number corresponds to how much that preference matters to them.)
         -compare list of ints to list of preferences: macros.PREFERENCES
      client.producttypes (list of ints, 0 for disinterested and 1 for interested)
         -compare list of ints to list of producttypes: macros.PRODUCTTYPES
"""


# product information 
#  produce a dictionary called "products"
""" import and configure dictionary of products. the keys should be the product names.
          each item in the dictionary should contain:
      product.ingredients (list of strings)
      product.type (string, one of the strings in macros.PRODUCTTYPES)
      product.price (float)
      product.unitprice ((float, unit) tuple) (i.e. (3.45, oz) or (2.34, gram))
      product.is (a dictionary which contains keys corresponding to each characteristic
        the imported product information contains 
        (i.e. product.is[("vegan", true), ("parabenfree", false)])
      product.ingrscore (float, initialized to 0.)
      product.valuescore (float, initialized to 0.)
      product.economyscore (float, initialized to 0.)
      product.splurgescore (float, initialized to 0.)
      product.hasbad (bool, tracks whether product contains ingredient which might 
        aggravate skin conditions)
"""


# other information
#  produce a dictionary called "chemtypes"
"""import and configure dictionary of chemical types.  the keys should be chemical type names.
          each item in the dictionary should contain:
      chemtype.ingrs (list of strings, those being the names of ingredients which 
        fall into that chemical type)
"""
#  using newly created chemtypes, produce a dictionary called "cond_info"
""" import and configure dictionary of conditions. the keys should be condition names.
          each item in the dictionary should contain:
      condition.good (list of strings, those being names of ingredients beneficial to 
        those with the condition)
      condition.bad (list of strings, those being names of ingredients harmful to those
        with the condition)
"""
#  using newly created chemtypes, produce a dictionary called "slider_info"
""" import and configure a dictionary of sliders. the keys should be slider names.
          each item in the dictionary should contain:
      slider.low (information necessary for clients for whom that slider is low)
        -slider.low.good
          -slider.low.good.ingredients, slider.low.good.prodtypes
        -slider.low.bad
          -slider.low.bad.ingredients, slider.low.bad.prodtypes
      slider.mid (information necessary for clients for whom that slider is in the middle)
        -same subgroups as with slider.low
      slider.high (information necessary for clients for whom that slider is high)
        -same subgroups as with slider.low
"""




        

# # # # # # # # #
# # ALGORITHM # #
# # # # # # # # #

# organizing information
"""
relevant resources available:
  -client
  -cond_info
  -slider_info

dealing with diagnosed conditions:
  -initialize two lists, "goodingrs" and "badingrs"
  -iterate through client.conds.  for each condition the client has:
    -union goodingrs with with condition.good
    -union badingrs with condition.bad
  -remove any elements in both goodingrs and badingrs from goodingrs 

dealing with sliders:
  -initialize "slideingrs" dictionary (will eventually associate ingredient names to a float)
  -initialize two lists: "slide_prodtypes_good" and "slide_prodtypes_bad" 
    (could eventually use to make recommendations to client beyond what they request)
  -establish score functions as follows:
    (plug into score function for good, negative score function for bad)
    -sliderlowscore will be a negative sigmoid which goes through (1,1), (5,0), and (10,-1)
    -slidermidscore will be bell curve which goes through (1,0), (5,1), and (10,0)
    -sliderhighscore will be sigmoid which goes through (1,-1), (5,0), and (10,1)
  -initialize variable curscore. for each slider with value v:
    -if v <= macros.SCORELOW_UPPER, set curscore == sliderlowscore(v)
    -for each ingredient in slider.low.good.ingredients:
      -if slide_ingrs[ingredient] already exists    ****(how to check? string similarity?)****
        add curscore to list associated with ingredient in slide_ingrs.
      -else, add ingredient to slideingrs with associated list containing curscore
    -for each ingredient in slider.low.bad.ingredients, do the same but with curscore * -1.
    -if v >= macros.SCOREMID_LOWER and v <= macros.SCOREMID_UPPER, set curscore == slidermidscore(v)
      -repeat same steps with slider.mid.good.ingredients and slider.mid.bad.ingredients
    -if v >= macros.SCOREHIGH_LOWER, set curscore == sliderhighscore(v)
      -repeat same steps with slider.high.good.ingredients and slider.high.bad.ingredients
  -for each ingredient in slideingrs, replace each value (list of scores) with the average 
    of the list elements
"""
# scoring products
"""
relevant resources available:
  -products
  -goodingrs
  -badingrs
  -slideingrs

setup:
-initialize a list for each product type the client is interested in
-for each product in products:
  if product.type is among the product types the client is interested in:
    add product to appropriate list
  initialize 4 variables for each list
    list_pricelow == product.price of first product in the list
    list_pricehigh == product.price of first product in the list
    list_unitpricelow == product.unitprice of first product in the list
    list_unitpricehigh == product.unitprice of first product in the list

to calculate ingredient score:
-for each list of the product type lists
  for each product in list:
    set product.hasbad to false
  -----------------------
      (next steps are for pricing scores)
      replace list_pricelow with min(list_pricelow, product.price)
      replace list_pricehigh with max(list_pricehigh, product.price)
      replace list_unitpricelow with min(list_unitpricelow, product.unitprice)
      replace list_unitpricehigh with max(list_unitpricehigh, product.unitprice)
  -----------------------
    initialize condgoodscore, condbadscore, and slidescore to 0
    for each ingredient in product.ingredients:
      -if ingredient is in goodingrs, add 1 to condgoodscore
       else if ingredient is in badingrs, add 1 to condbadscore
         and set product.hasbad to true
      -if ingredient is in slideingrs, add slideingrs[ingredient] to slidescore
    linear equation to calculate product.ingrscore is as follows:
    product.ingrscore == product.condgoodscore 
                     - macros.BADWEIGHT*product.condbadscore 
                     + macros.SLIDEWEIGHT*product.slidescore

to calculate pricing scores:
-for each list of the product type lists
  initialize pricediff to be list_pricehigh - list_pricelow
  initialize unitpricediff to be list_unitpricehigh - list_unitpricelow
  for each product in list:
    product.splurgescore = (product.price - list_pricelow) / pricediff
    product.economyscore = 1 - product.splurgescore
    product.valuescore = 1 - (product.unitprice - list_unitpricelow) / unitpricediff
 
"""
# producing recommendations
"""
relevant resources available:
  -lists of products by product type
    containing:
    -product.ingrscore (score of how good the ingredients are for the client)
    -product.economyscore (score of how inexpensive the product is relative to 
      other products of the same product type)
    -product.valuescore (score of how good the unit price of the product is relative 
      to other products of the same product type)
    -product.splurgescore (score of how expensive the product is relative to other 
      products of the same type)
    -product.hasbad (whether or not the product contains ingredients which could 
      aggravate one of the client's diagnosed skin conditions)

to calculate recommendations for each product type the client is interested in:
  for each product type list:
    for each product in list:
      product.economyscore == product.economyscore * macros.PRICEWEIGHT 
                              + product.ingrscore * macros.INGRWEIGHT
      product.valuescore == product.valuescore * macros.PRICEWEIGHT 
                              + product.ingrscore * macros.INGRWEIGHT
      product.splurgescore == product.splurgescore * macros.PRICEWEIGHT 
                              + product.ingrscore * macros.INGRWEIGHT
    for economical option:
      recommend product in list with maximal product.economyscore
    for value option:
      recommend product in list with maximal product.valuescore
    for splurge option:
      recommend product in list with maximal product.splurgescore
"""
