def create_bx(probabilities):
    bx = [(probabilities[0][0], 0.0)]

    for i, item in enumerate(probabilities):
        res = sum([item[1] for item in probabilities[:i]])
        bx.append((item[0], res))

    del bx[1]

    return bx


def generate_codes(probabilities, bx):
    binarized = [(item[0], get_binary_repr(item[1])) for item in bx]
    binarized[0] = (binarized[0][0], '0.0000000000000000000000000000000000000')
    res = [(item[0], item[1][2:ceil(abs(log2(probabilities[i][1]))) + 2]) for i, item in
           enumerate(binarized)]

    codes = dict({item[0]: item[1] for item in res})

    return codes