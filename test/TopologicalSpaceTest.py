import unittest
import numpy as np

from src.TopologicalSpace import TopologicalSpace
from src.Axis import Axis

class TestTopologicalSpace(unittest.TestCase):
    def test_init(self):
        axes = (Axis("theta", -1.0, 0.0, 1.), Axis("theta_dot", -1.0, 0.0, 1.), Axis("x", -2.0, 0.0, 1.))
        self.topologicalSpace = TopologicalSpace(*axes)
        print(len(self.topologicalSpace.astablishment_space))
        print(self.topologicalSpace.astablishment_space)

    def test_posAS2posTS(self):
        axes = (Axis("theta", -6.0, 0.0, 1.), Axis("theta_dot", -5.0, 0.0, 1.), Axis("x", -4.0, 0.0, 1.))
        self.topologicalSpace = TopologicalSpace(*axes)

        pos_TS = [1, 3, 2]
        pos_AS = self.topologicalSpace.pos_TS2pos_AS(pos_TS)
        pos_TS_ans = tuple([np.array([val]) for val in pos_TS])
        self.assertEqual(pos_TS_ans, self.topologicalSpace.pos_AS2pos_TS(pos_AS))

    # def test_set_coodinate_space(self):
    #     axes = (Axis("theta", -6.0, 0.0, 1.), Axis("theta_dot", -5.0, 0.0, 1.), Axis("x", -4.0, 0.0, 1.))
    #     self.topologicalSpace = TopologicalSpace(*axes)
    #     print("self.topologicalSpace.coodinate_space")
    #     print(self.topologicalSpace.coodinate_space)

if __name__ == "__main__":
    unittest.main()