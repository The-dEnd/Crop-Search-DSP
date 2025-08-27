#!/usr/bin/python3
#this file keeps track of the getMeasureState/setMeasureState booleans, used to measure the size of a die; by default, this would request a circular import, hence the variables have been placed in a specific file

class MeasureState:
    setMeasureState = False #boolean keeping track on whether the initial measure ruler is set or not
    getMeasureState = False #boolean keeping track on whether the final measure ruler is set or not