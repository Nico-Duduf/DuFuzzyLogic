# -*- coding: utf-8 -*-

from dufuzzylogic import *

def testQuantifiers():
    logic = FuzzyLogic()
    q = FuzzyQuantifier.DOUBLE_MINUS
    print(q)
    mySet = logic.newSet( "Name", 15, 20 )
    contains = mySet.FSet_contains( 16, q )
    print( contains.veracity ) # 1 
    logic.FLogic_IF( contains )
    print( logic.veracity.veracity )

testQuantifiers()