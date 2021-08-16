import random
import numpy as np
import quanguru.QuantumToolbox.states as qst
import quanguru.QuantumToolbox.linearAlgebra as qlina

def spinCoherent(theta, phi):
    # spin coherent state of a qubit, by definition already normalized
    plusComponent = np.cos(theta/2)*qst.basis(2, 0)
    minusComponent = (np.e**(-1j*phi))*np.sin(theta/2)*qst.basis(2, 1)
    return plusComponent + minusComponent

def spinCoherentComposite(theta, phi, N=1):
    # spin coherent state of N qubits. obtained by the tensor product normalized states, so normalized
    return qlina.tensorProd(*[spinCoherent(theta, phi) for ind in range(N)]) if N > 1 else spinCoherent(theta, phi)

def spinCoherentRange(thetas, phis, N=1):
    # spin coherent states for N qubits for given list of angles
    states = []
    for theta in thetas:
        for phi in phis:
            states.append(spinCoherentComposite(theta, phi, N))
    return states

def _determineAngle(cNumber):
    # phase of a unit complex number
    angle = np.arccos(np.real(cNumber))
    return -angle if np.imag(cNumber) < 0 else angle

def _gaussianRNDC(normalise=False):
    # complex number with Gaussian random components
    c = random.gauss(0, 1) + 1j*random.gauss(0, 1)
    return c/np.abs(c) if normalise else c

def _randomPureState(dimension):
    # random pure state for a given dimension, i.e. each components coefficient is a Gaussian random complex number
    return qst.normalise(sum([_gaussianRNDC()*qst.basis(dimension, i) for i in range(dimension)]))

def _randomProdStateOfEqW(dims):
    # random product state of given dimensions. tensor product of normalized states, so should ideally be normalized
    states = [_randomPureState(d) for d in dims]
    return qlina.tensorProd(*states)

def _randomProdStateOfRndW(dims):
    # random product state of given dimensions
    states = [_gaussianRNDC()*_randomPureState(d) for d in dims]
    return qst.normalise(qlina.tensorProd(*states))

def _randomProdStateOfSameRndW(n=1, dim=2):
    # random product state of given dimensions
    state = _randomPureState(dim)
    states = [_gaussianRNDC()*state for d in range(n)]
    return qst.normalise(qlina.tensorProd(*states))

def _randomSpinCoherentRnd(n=1):
    rndThetaAngle = _determineAngle(_gaussianRNDC(normalise=True))
    rndPhiAngle = _determineAngle(_gaussianRNDC(normalise=True))
    return spinCoherentComposite(rndThetaAngle, rndPhiAngle, N=n)

def _randomSpinCoherentPure(n=1, dim=2):
    state = _randomPureState(dim)
    return qlina.tensorProd(*[state for i in range(n)]) if n > 1 else state
