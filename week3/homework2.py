from homework1 import test

# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")

    # below test read_number function, make sure reading the number part is ok
    test("1") # only integer without symbol, integer part in read_number function
    test("23.4567") # only float without symbol, integer + float_dot + float_number part in read_number function

    # below test plus and minus function, make sure the +, - part is ok
    # test("-1") # only integer without symbol, first integer in times and divide function, minus part in plust_minus function
    # test("-23.4567") # only float without symbol, actually not necessary because it is same as above for testing
    test("2+3") # plus function, first integer in times and divide function, plus function in first integer and plus function in second integer.
    test("2-3") # minus function
    test("-1+3") # first is minus mix plus and minus function
    test("3+4-1") # first is plus mix plus and minus function
    test("1.2+2.3-0.1") # mix plus and minus for float numbers actually we don't need to test this but just in case

    # # below test times and divide function, make sure * , / part is ok
    test("2*3") # times function
    test("2/3") # divide function
    test("-2*3") # first minus, times function
    test("-2/3") # first minus, divide function
    test("4*5/2") # mix times and divide function, times first
    test("4/2*6") # mix times and divide function, divide first
    test("4/3*6") # mix times and divide function, when first divide function is not divided perfectly
    test("4+4/3*6") # mix plus and times and divide function, put plus first
    test("4/3*6+4") # mix plus and times and divide function, put plus last
    test("-3-4/3*6+4") # mix plus and times and divide function, binded with plus and minus
    test("-3-4/3*6+4-7*5") # mix plus and several times and divide function
    # test("-3.1-4.2/3.5*6.2+4.9-7.4*5.1") # mix plus and several times and divide function for float not actually needed but just in case
    print("==== Test finished! ====\n")

if __name__ == "__main__":
  run_test()