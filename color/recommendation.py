import pandas as pd
from face import skin
from complexion import analyze,get_complexion,undertone
from combination import palette

def estimate():

    hex,_,_=skin("man2.jpg")
    comp,under,lab=analyze(hex)
    print("Hex color : ",hex)
    print("Complexity : ",comp)
    print("Undertone : ",under)
    k=palette()

    if comp=='dark' and under=='warm':
        print(k['dark'] & k['warm'])
    elif comp=='dark' and under=='cool':
        print(k['dark'] & k['cool'])
    elif comp=='dark' and under=='neutral':
        print(k['dark'] & k['neutral'])
    
    elif comp=='medium' and under=='warm':
        print(k['medium'] & k['warm'])
    elif comp=='medium' and under=='cool':
        print(k['medium'] & k['cool'])
    elif comp=='medium' and under=='neutral':
        print(k['medium'] & k['neutral'])

    elif comp=='light' and under=='warm':
        print(k['light'] & k['warm'])
    elif comp=='light' and under=='cool':
        print(k['light'] & k['cool'])
    else: 
        print(k['light'] & k['neutral'])

if __name__ == "__main__":

    estimate()

