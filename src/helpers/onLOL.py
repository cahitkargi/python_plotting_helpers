import numpy as np

def cutAlist(listGiven, position = None, cut = None, startPosition = 0):
    r"""
    Function to truncate a list at the given position or position divided buy some cut. The later option is introduced
    to create flexibility for time traces with different step sizes, so that if we give position as the time and the
    cut as the step time (of the particular time trace), we would be truncating list for the same time not same # of
    elements.
    """
    listReturn = listGiven
    if position is not None:
        if cut is None:
            listReturn = listGiven[startPosition:position]
        else:
            ran = int(position/cut)+1
            listReturn = listGiven[startPosition:ran]
    return listReturn if len(listReturn) > 0 else listGiven[0:1]

def cutALOL(listOfLists, position = None, cuts = None, startPosition = 0):
    r"""
    Same as :func:`cutAList` but for list of lists and calls `cutAList` for each sub-list. `cut` in this case can be a
    list.
    """

    if isinstance(cuts, (list, np.ndarray)):
        listOfLists = [cutAlist(li, position, cuts[ind], startPosition) for ind, li in enumerate(listOfLists)]
    else:
        listOfLists = [cutAlist(li, position, cuts, startPosition) for li in listOfLists]
    return listOfLists

def atEvery(n, ofList):
    r"""
    Dilute a list by sampling at every `n`th element.

    Parameters
    ----------
    n : int
        sample rate, for example `n=3` will sample the indices `0, 3, 6, ...` (at every n*m for non-negative integer m)
    ofList : List[List]
        A list of lists
    """

    return [ofList[i] for i in range(len(ofList)) if i%n == 0]

def maxLOL(listOfLists, position = None, cuts = None, minOf=False, startPosition = 0):
    r"""
    Returns the maximum value in a list of lists and also returns minimum `if minOf`.

    Parameters
    ----------
    listOfLists : List[List]
        A list of lists, and the elements in the list should support `__leq__` and `__geq__` among each other.
    minOf : bool, optional
        also finds the min `if minOf`, by default `False`.
    position: float, optional
        Index to truncate the list, or a number (like time) to be divided by cut (like step size) to determine index
    cuts: list, optional
        A list of cut values (like step size)
    """
    listOfLists = cutALOL(listOfLists, position, cuts, startPosition)
    maxVal = max(max(l) for l in listOfLists)
    return (maxVal, min(min(l) for l in listOfLists)) if minOf else maxVal

def minLOL(listOfLists, position = None, cuts = None, maxOf=False, startPosition = 0):
    r"""
    Returns the minimum value in a list of lists and also returns maximum `if minOf`.

    Parameters
    ----------
    listOfLists : List[List]
        A list of lists, and the elements in the list should support `__leq__` and `__geq__` among each other.
    minOf : bool, optional
        also finds the max `if minOf`, by default `False`.
    position: float, optional
        Index to truncate the list, or a number (like time) to be divided by cut (like step size) to determine index
    cuts: list, optional
        A list of cut values (like step size)
    """

    listOfLists = cutALOL(listOfLists, position, cuts, startPosition)
    minVal = min([min(l) for l in listOfLists])
    # if maxOf:
    #     maxVal = max([max(l) for l in listOfLists])
    return (max([max(l) for l in listOfLists]), minVal) if maxOf else minVal

def _isAbs(a, b):
    return abs(a-b)
def _isDif(a, b):
    return a-b

def avgAbsErrLOL(list1, list2, position = None, cuts = None, absErr = True, startPosition = 0):
    r"""
    Calculates the average of point-wise (absolute, by default) errors for two lists at the same index of two lists of
    lists. `If absErr is False`, then absolute is not used.
    Each list have to be the same length,
    and each sub-list at the same index also have to be the same length.

    Parameters
    ----------
    list1 : List[List]
        A list of lists
    list2 : [type]
        A list of lists
    absErr: bool
        `If absErr is False`, calculates the average of differences, by default `True`.
    position: float, optional
        Index to truncate the list, or a number (like time) to be divided by cut (like step size) to determine index
    cuts: list, optional
        A list of cut values (like step size)

    Returns
    -------
    List
        A list of averaged point-wise absolute error
    """

    assert len(list1) == len(list2), "Given lists have different lengths"
    list1 = cutALOL(list1, position, cuts, startPosition)
    list2 = cutALOL(list2, position, cuts, startPosition)
    difFunc = _isAbs if absErr else _isDif
    errList = []
    for ii in range(len(list1)):
        assert len(list1[ii]) == len(list2[ii]), f"Sub-lists at index {ii} have different lengths"
        er1 = [difFunc(list1[ii][jj], list2[ii][jj]) for jj in range(len(list1[ii]))]
        # for jj in range(len(list1[ii])):
        #     if absErr:
        #         er1.append(abs(list1[ii][jj]-list2[ii][jj]))
        #     else:
        #         er1.append(list1[ii][jj]-list2[ii][jj])
        errList.append(sum(er1)/len(er1))
    return errList

def meanLOL(listOfLists, position = None, cuts = None, startPosition = 0):
    r"""[summary]

    Parameters
    ----------
    listOfLists : List[List]
        A list of lists
    position: float, optional
        Index to truncate the list, or a number (like time) to be divided by cut (like step size) to determine index
    cuts: list, optional
        A list of cut values (like step size)

    Returns
    -------
    List
        A list of mean of each sub-list
    """

    # lll = []
    # listOfLists = cutALOL(listOfLists, position, cuts)
    # for ii in range(len(listOfLists)):
    #     lll.append(sum(listOfLists[ii])/len(listOfLists[ii]))
    # return lll
    listOfLists = cutALOL(listOfLists, position, cuts, startPosition)
    return [sum(lil)/len(lil) for lil in listOfLists]

def divideLOL(listOfLists, value, position = None, cuts = None, startPosition = 0):
    r"""
    Divide every sub-list of a list with the given dim value.

    Parameters
    ----------
    listOfLists : List[List]
        A list of lists
    value : float
        value to divide the sub-lists
    position: float, optional
        Index to truncate the list, or a number (like time) to be divided by cut (like step size) to determine index
    cuts: list, optional
        A list of cut values (like step size)
    """

    listOfLists = cutALOL(listOfLists, position, cuts, startPosition)
    return [li/value for li in listOfLists]
