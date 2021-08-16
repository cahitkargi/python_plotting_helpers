import numpy as np
from numpy.polynomial.polynomial import polyfit, polyval
from quanguru.QuantumToolbox import expectation, mat2Vec
from .specialStates import _determineAngle #pylint:disable=import-error

def calcEigenPhases(vals):
    return sorted([_determineAngle(v) for v in vals])

def bunchEigenPhases(vals, vecs, reductionOps=[], eigPhases = True): #pylint:disable=dangerous-default-value
    out = [[] for op in range(2**len(reductionOps))]
    out2 = [[] for op in range(2**len(reductionOps))]
    for ind in range(len(vecs)):
        expects = [expectation(op, mat2Vec(vecs[:, ind])) > 0 for op in reductionOps]
        out2[sum(expects)].append(mat2Vec(vecs[:, ind]))
        toApp = _determineAngle(vals[ind]) if eigPhases else np.real(vals[ind])
        out[sum(expects)].append(toApp)
        #out[sum(expects)].append(_determineAngle(vals[ind]))
    return [sorted(li) for li in out], out2

def polyUnfold(vals, degree = 9):
    steps = np.arange(0, len(vals)) + 1
    polyCoef = polyfit(vals, steps, degree)
    unfolded = polyval(vals, polyCoef)
    return unfolded

def calculateSpacings(l1):
    return [(l1[ind+1] - l1[ind]) for ind in range(len(l1)-1) if (l1[ind+1] - l1[ind]) > 1e-10]
