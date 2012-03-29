from decimal import *

def convert(num):
    getcontext().prec = 3
    values = [ 1000000000,1000000,1000,100 ]    
    names = ['Billion','Million','Thousand','Hundred']
    data = dict(zip(names,values))

    for name in names:
        temp = Decimal(num) / data[name]
        if temp >= 1:
            return converter(temp,name)
    return str(num)

    


def converter(num,word):
    if num == 1:
        front = 'One'
    else:
        front = str(num)
    result = front + ' '+word
    return result


    
