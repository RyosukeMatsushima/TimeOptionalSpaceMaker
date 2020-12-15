import numpy as np
from tempfile import mkdtemp
import os.path as path
from tqdm import tqdm

from src.Axis import Axis
from src.submodule.PhysicsSimulator.SinglePendulum.SinglePendulum import SinglePendulum

'''
# name space
pos_in_astablishment_space pos_AS
pos_in_topological_space pos_TS
coodinate
'''

class TopologicalSpace:
    def __init__(self, *axes: Axis):
        print("init TopologicalSpace")
        self.axes = axes
        self.set_astablishment_space()
        self.set_posTS_space()
        self.element_count = self._element_count(self.axes)

        # parameter set
        self.delta_t = 0.001
        print("init TopologicalSpace end")

    def set_astablishment_space(self):
        self.element_count = self._element_count(self.axes)
        filename = path.join(mkdtemp(), 'astablishment_space.dat')
        self.astablishment_space = np.memmap(filename, dtype='float32', mode='w+', shape=self.element_count)

    def set_posTS_space(self):
        print("\n set_posTS_space \n")
        pos_AS_space = np.arange(self.element_count)
        shape = tuple([len(axis.elements) for axis in self.axes])
        pos_TS_space = pos_AS_space.reshape(shape)

        filename = path.join(mkdtemp(), 'posTS_space.dat')
        self.posTS_space = np.memmap(filename, dtype='int32', mode='w+', shape=shape)
        self.posTS_space = pos_TS_space

        del pos_AS_space, pos_TS_space, shape

        print("\n set_posTS_space end \n")

    def set_coodinate_space(self):
        print("\n set_pos_coodinate_space \n")
        shape = [len(axis.elements) for axis in self.axes]
        shape += [len(self.axes)]

        filename = path.join(mkdtemp(), 'coodinate_space.dat')
        self.coodinate_space = np.memmap(filename, dtype='float32', mode='w+', shape=shape)

        print("\n set_pos_coodinate_space end \n")

    def _element_count(self, axes):
        val = 1
        for axis in axes:
            val *= len(axis.elements)
        return val

    def get_val(self, coodinate):
        pos_TS = self.coodinate2pos_TS(coodinate)
        return self.astablishment_space[self.pos_TS2pos_AS(pos_TS)]

    def write_val(self, coodinate, val):
        pos_TS = self.coodinate2pos_TS(coodinate)
        self.astablishment_space[self.pos_TS2pos_AS(pos_TS)] = val

    def pos_TS2pos_AS(self, pos_TS):
        l = self.posTS_space[:]
        for index in pos_TS:
            l = l[index]
        return l

    def pos_AS2pos_TS(self, pos_AS):
        #TODO: check out of chenge
        return np.where(self.posTS_space == pos_AS)

    def _times_all(self, l):
        val = 1
        for i in l:
            val *= i
        return val

    def pos_TS2coodinate(self, pos_TS):
        return [self.axes[i].num2val(pos_TS[i]) for i in range(len(self.axes))]

    def coodinate2pos_TS(self, coodinate):
        if len(coodinate) is not len(self.axes):
            raise TypeError("size of coodinate and number of axes is not same")
        pos_TS = []
        for i in range(len(self.axes)):
            pos_TS.append(self.axes[i].val2num(coodinate[i]))
        return pos_TS

    def coodinate2pos_AS(self, coodinate):
        return self.pos_TS2pos_AS(self.coodinate2pos_TS(coodinate))

    def is_edge_of_TS(self, pos_TS):
        if len(pos_TS) is not len(self.axes):
            raise TypeError("size of element_num and number of axes is not same")
        pos = np.array(pos_TS)
        min_edge = np.full(len(self.axes), 0, dtype=int)
        max_edge = np.array([len(axis.elements) - 1 for axis in self.axes])
        return True in (pos == min_edge) or True in (pos == max_edge)
