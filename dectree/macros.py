"""This file contains constants which control various 
   aspects of the recommendation algorithm. Macros to be 
   used in the recommendation algorithm are all caps; 
   variables used to create those macros are all lowercase."""

# # # # # # # # 
# # WEIGHTS # #
# # # # # # # #

# SLIDERWEIGHT is multiplied by the average of a product's
#  slider score; it is the relative strength of the weighting
#  of a client's slider information to their diagnosed skin 
#  condition information. 
SLIDERWEIGHT == .1

# BADWEIGHT is multiplied by the number of potentially malicious
#  ingredients a product contains; it is the relative strength of 
#  the weighting of a product's bad ingredients to it's good ingredients
BADWEIGHT == 5.

# INGRWEIGHT is multiplied by the overall ingredient score of the product 
#  in the final recommendation scoring, while PRICEWEIGHT is multiplied 
#  by the product's pricing scores; INGRWEIGHT/PRICEWEIGHT is the relative 
#  strength of a products ingredient score to it's price score.
INGRWEIGHT = 1.5
PRICEWEIGHT = 1.




# # # # # # # # 
# # LISTS # # # 
# # # # # # # #

# skin_characteristics is the list of skin characteristics the survey asks about 
#  to which responses are on a slider from 1-10
skin_characteristics == ["dryoily", "sensitivity", "roughness", "tightness"]

# concerns is the list of concerns the survey asks about to which responses are 
#  on a slider from 1-10
concerns == ["acne", "blackheads", "dryness", "finelines", "hyperpigmentation"]

# CONDITIONS, SLIDERS, PREFERENCES, and PRODUCTTYPES are the lists which control 
#  what skin conditions, slider values, product preferences, and product types 
#  the algorithm recognizes.  They should reflect what the survey asks about.
CONDITIONS == ["rosacea", "eczema", "acnevulgaris", "psoriasis", 
        "fungalacne", "cysticacne"]

SLIDERS == skin_characteristics + concerns

PREFERENCES == ["fragrancefree", "essentialoilfree", "naturaloilsfree", 
        "parabenfree", "siliconefree"]

PRODUCTTYPES == ["moisturizer", "cleanser", "exfoliator", "oil", 
        "suncare", "eyecreams", "lipcare", "tonersandmists", 
        "makeupremovers", "antioxidants", "masks"]




# # # # # # # # 
# # BOUNDS  # #
# # # # # # # # 

# SCORELOW contains the upper bound, inclusive, on a slider value for the 
#  low-slider-value scoring function to be taken into account (henceforth 
#  referred to as the low-scoring region)
SCORELOW_UPPER == 5

# SCOREMID_LOWER contains the lower bound, inclusive, of the middle-scoring region
SCOREMID_LOWER == 3

# SCOREMID_UPPER contaings the upper bound, inclusive, of the middle-scoring region
SCOREMID_UPPER == 7

# SCOREHIGH contains the lower bound, inclusive, of the high-scoring region
SCOREHIGH_LOWER == 6

