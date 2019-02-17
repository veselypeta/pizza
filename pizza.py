import numpy


def parseFile(filename):
    with open(filename, 'r') as inputData:
        rawData = [x.strip('\n') for x in inputData.readlines()]  # remove the newlines from each line as they are read in
        row_number, col_number, min_ingredients, max_size = tuple(
            map(int, rawData[0].split(' ')))  # assign the numeber values to the variable
        pizza = [[rawData[x][y]
                  for y in range(col_number)]for x in range(1, row_number+1)]
        return pizza, row_number, col_number, min_ingredients, max_size

def prettyPrintPizza(pizza):
    print("-" *(len(pizza[0])+2))
    for row in pizza:
        print("|"+"".join(row)+"|")
    print("-" *(len(pizza[0])+2))

def getSlice(row_start, row_end, col_start, col_end, pizza):
    try:
        return [pizza[x][y] for x in range(row_start, row_end) for y in range(col_start, col_end) if '0' not in pizza[x][y]]
    except IndexError:
        return None

def is_minimum_condition_met(pizza_slice, min_ingredients, max_size):
    mushrooms = pizza_slice.count('M')
    tomatoes = pizza_slice.count('T')
    # make sure the conditions for a valid pizza slice are met
    if mushrooms >= min_ingredients and tomatoes >= min_ingredients and len(pizza_slice) <= max_size:
        return True
    else:
        return False

# since all pizza slices must be square/rectangular
# it is useful to know what kind of slices we can make
def get_factors(max_size, min_ingredients):
    return [(x, y) for x in range(1, max_size+1) for y in range(1, max_size+1) if x*y <= max_size and x*y >= 2*min_ingredients]

def score_slice(pizza_slice, min_ingredients, max_size):
    # if slice is invalid then gets 0 --- i.e. not got enough tomatoes or mushrooms
    # otherwise it's score is based on it's length
    # therefore 'longer' pizza slices are prefered.
    if pizza_slice is None:
        return 0
    elif is_minimum_condition_met(pizza_slice, min_ingredients, max_size):
        return len(pizza_slice)
    else:
        return 0

def set_definite_slice(pizza, rstart, rend, cstart, cend):
    for i in range(rstart, rend):
        for j in range(cstart, cend):
            pizza[i][j] = '0'

def getOptimalSlice(pizza, row_index, col_index, min_ingredients, max_size):
    slice_shapes = get_factors(max_size, min_ingredients) # get all possible pizza shapes
    actualSlices = [getSlice(row_index, row_index + x, col_index, col_index+y, pizza) for x, y in slice_shapes]
    slice_scores = [score_slice(x, min_ingredients, max_size) for x in actualSlices]
    # zip together the slice, the slice-scores along with the actual shape
    ziped_scores = sorted(list(zip(actualSlices, slice_scores, slice_shapes)), key=lambda x : x[1], reverse = True)
    try:
        # this is the best slice that we can apply, we need to keep track of the slice
        best_slice = ziped_scores[0]
        ### this is super bodge and i don't like it -- it's using a reference to a list to overwrite it 
        set_definite_slice(pizza, row_index, best_slice[2][0], col_index, best_slice[2][1]) # apply the slice to the pizza
        return (row_index, best_slice[2][0], col_index, best_slice[2][1])
    except IndexError:
        return None




def __main__(testFile):
    pizza, row_number, col_number, min_ingredients, max_size = parseFile(
        filename=testFile)
    print("Number of row = {}, number of columns = {}, minimum ingredients = {}, max slice size = {}".format(row_number, col_number, min_ingredients, max_size))
    print(getOptimalSlice(pizza, 0, 0, min_ingredients, max_size))
    allSlices = [getOptimalSlice(pizza, x, y, min_ingredients, max_size) for x in range(row_number) for y in range(col_number)]
    prettyPrintPizza(pizza)
    print(allSlices)


    # slices = [getOptimalSlice(pizza, x, y, min_ingredients, max_size) for x in range(row_number) for y in range(col_number) if pizza[x][y] != '0']
    test_slice = getSlice(row_start=0, row_end=1,
                          col_start=0, col_end=2, pizza=pizza)



__main__("small.in")

