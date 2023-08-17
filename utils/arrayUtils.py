def repeat(value, iterations, stepSize=0):
    array = []
    for i in range(iterations):
        array.append(value + stepSize * i)
    return array
