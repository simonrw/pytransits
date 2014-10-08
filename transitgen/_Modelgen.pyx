cdef extern from "Model.h":
    cdef cppclass Model:
        int id
        int submodel_id
        double period
        double epoch
        double a
        double rs
        double i
        double rp
        double mstar
        double c1
        double c2
        double c3
        double c4
        double teff




cdef class PyModel:
    '''
    Handles the model parameters for the 
    generation
    '''
    cdef Model *thisptr
    def __cinit__(self):
        self.thisptr = new Model()

    def __dealloc__(self):
        del self.thisptr

    property id:
        def __get__(self):
            return self.thisptr.id

        def __set__(self, id):
            self.thisptr.id = id


    property submodel_id:
        def __get__(self):
            return self.thisptr.submodel_id

        def __set__(self, submodel_id):
            self.thisptr.submodel_id = submodel_id

    property period:
        def __get__(self):
            return self.thisptr.period

        def __set__(self, period):
            self.thisptr.period = period

    property epoch:
        def __get__(self):
            return self.thisptr.epoch

        def __set__(self, epoch):
            self.thisptr.epoch = epoch

    property a:
        def __get__(self):
            return self.thisptr.a

        def __set__(self, a):
            self.thisptr.a = a

    property rs:
        def __get__(self):
            return self.thisptr.rs

        def __set__(self, rs):
            self.thisptr.rs = rs

    property i:
        def __get__(self):
            return self.thisptr.i

        def __set__(self, i):
            self.thisptr.i = i

    property rp:
        def __get__(self):
            return self.thisptr.rp

        def __set__(self, rp):
            self.thisptr.rp = rp

    property mstar:
        def __get__(self):
            return self.thisptr.mstar

        def __set__(self, mstar):
            self.thisptr.mstar = mstar

    property c1:
        def __get__(self):
            return self.thisptr.c1

        def __set__(self, c1):
            self.thisptr.c1 = c1

    property c2:
        def __get__(self):
            return self.thisptr.c2

        def __set__(self, c2):
            self.thisptr.c2 = c2

    property c3:
        def __get__(self):
            return self.thisptr.c3

        def __set__(self, c3):
            self.thisptr.c3 = c3

    property c4:
        def __get__(self):
            return self.thisptr.c4

        def __set__(self, c4):
            self.thisptr.c4 = c4

    property teff:
        def __get__(self):
            return self.thisptr.teff

        def __set__(self, teff):
            self.thisptr.teff = teff

# Wrap the vector class
from libcpp.vector cimport vector
cimport numpy as np
import numpy as np

# Utility function to convert from numpy array to vector
cdef vector[double] arrayToVector(np.ndarray[np.double_t,ndim=1] array):
    cdef long size = array.size
    cdef vector[double] vec
    cdef long i
    for i in range(size):
        vec.push_back(array[i])

    return vec

cdef np.ndarray[np.double_t, ndim=1] vectorToArray(vector[double] v):
    cdef int size = v.size()

    out = np.zeros(size)
    for i in range(size):
        out[i] = v[i]

    return out

# Now wrap the main generation function
cdef extern from "GenerateModel.h":
    cdef vector[double] GenerateSynthetic(vector[double] jd, Model m)

cdef Model convertModel(PyModel m):
    cdef Model out
    out.id = m.id
    out.submodel_id = m.submodel_id
    out.period = m.period
    out.epoch = m.epoch
    out.a = m.a
    out.rs = m.rs
    out.i = m.i
    out.rp = m.rp
    out.mstar = m.mstar
    out.c1 = m.c1
    out.c2 = m.c2
    out.c3 = m.c3
    out.c4 = m.c4
    out.teff = m.teff
    return out

def _check_types(jd, m):
    if not isinstance(m, PyModel):
        raise TypeError("model object must be of type PyModel")

    if type(jd) != np.ndarray:
        raise TypeError("jd must be a numpy array")

    return True

def PyGenerateSynthetic(jd, m):
    _check_types(jd, m)
    cdef vector[double] vec_jd = arrayToVector(jd)
    cdef Model model = convertModel(m)

    cdef vector[double] flux = GenerateSynthetic(vec_jd, model)
    return vectorToArray(flux)
