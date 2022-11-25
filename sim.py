from __future__ import annotations
###
import numpy as np
from scipy.spatial.transform import Rotation
import json
###
from gui import plot_rubik


class Simulator:
    coordinates: np.ndarray
    sticky_cubes: list

    def __init__(self, coordinates, sticky_cubes) -> None:
        self.coordinates = np.array(coordinates)
        self.sticky_cubes = sticky_cubes

    def take_action(self, ind: int, axis: int, alpha_ind: int) -> None:
        alpha = alpha_ind * 90
        new_coordinates = self.coordinates.copy()
        # solve in forward
        if self.is_knee(ind):
            print(self.coordinates[ind-1], self.coordinates[ind], self.coordinates[ind+1], axis)
            if self.is_on_axis(ind, axis):
                self.rotate_knee(new_coordinates, ind, axis, alpha, -1)
            elif self.is_on_axis(ind-1, axis):
                self.rotate_knee(new_coordinates, ind, axis, alpha)
        else:
            # self.solve_in_direction(new_coordinates, ind, axis, alpha)
            plot_rubik(Simulator(new_coordinates, self.sticky_cubes))
            # solve in backward
            # self.solve_in_direction(new_coordinates, ind, axis, alpha, -1)
            plot_rubik(Simulator(new_coordinates, self.sticky_cubes))

        if self.is_valid_coordinates(new_coordinates):
            self.coordinates = new_coordinates

    def solve_in_direction(self, coordinates: np.ndarray, ind: int, axis: int, alpha: int, step=1) -> None:
        pn_pri = 0 if step == 1 else -1
        if self.is_sticky_to_next(ind+pn_pri) and self.is_on_axis(ind+pn_pri, axis):
            loop_end = len(self.coordinates)-1 if step == 1 else 0
            for f_ind in range(ind+step, loop_end, step):
                if self.is_knee(f_ind):
                    self.rotate_knee(coordinates, f_ind, axis, alpha, step)
                    return
                if not self.is_sticky_to_next(f_ind+pn_pri):
                    return 
        # return coordinates

    def rotate_knee(self, coordinates: np.ndarray, knee_ind: int, axis: int, alpha: int, step=1) -> None:
        # end = 0 if step == -1 else len(self.coordinates)
        coordinates[knee_ind+step::step] = self.rotate_cubes(
            coordinates[knee_ind+step::step],
            axis,
            alpha
        )
        
    def is_on_axis(self, first_ind: int, axis: int) -> bool:
        subs = self.coordinates[first_ind] - self.coordinates[first_ind+1]
        return subs[axis] != 0

    def is_knee(self, ind: int) -> bool:
        if ind == 0 or ind == len(self.coordinates) - 1:
            return False
        prev, next = self.coordinates[ind-1], self.coordinates[ind+1]
        return not self.is_in_one_axis(prev, next)

    def is_sticky_to_next(self, ind: int) -> bool:
        return [ind, ind+1] in self.sticky_cubes

    @staticmethod
    def is_in_one_axis(c1: np.ndarray, c2: np.ndarray) -> bool:
        subs = c1 - c2
        nonzeros = np.count_nonzero(subs)
        return nonzeros == 1

    @staticmethod
    def rotate_cubes(cs: np.ndarray, axis: int, alpha: int) -> np.ndarray:
        assert alpha in [90, 180, 270]
        assert axis in range(3)
        axis_letter = {0: 'x', 1: 'y', 2: 'z'}
        r = Rotation.from_euler(axis_letter[axis], alpha, degrees=True)
        rotated = r.apply(cs).round(0)
        return rotated

    @staticmethod
    def is_valid_coordinates(coordinates: np.ndarray) -> bool:
        return len(np.unique(coordinates, axis=0)) == 27

    def serialize_to_json_str(self) -> str:
        output_dict = {
            "Coordinates": self.coordinates.tolist(),
        }
        return json.dumps(output_dict)

    def deep_copy(self) -> Simulator:
        return Simulator(self.coordinates.copy(), self.sticky_cubes)


class Interface:
    def evolve(self, state: Simulator, action: tuple):
        if type(action[0]) is not int:
            raise ("index is not an int")
        if type(action[1]) is not int:
            raise ("alpha is not an int")
        if self.is_valid_action(action):
            raise ("action is not valid")
        state.take_action(action)

    def perceive(self, state: Simulator) -> str:
        return state.serialize_to_json_str()

    def copy_state(self, state: Simulator) -> Simulator:
        return state.deep_copy()

    def goal_test(self, state: Simulator) -> bool:
        center = state.coordinates.mean(axis=0)
        rel_coordinates = (state.coordinates - center)
        rel_coordinates = np.abs(state.coordinates - center)
        rel_coordinates[rel_coordinates == 1] = 0
        return rel_coordinates.sum() == 0

    @staticmethod
    def is_valid_action(action):
        if action[0] not in range(27) or action[1] not in range(3):
            return False
        return action[2] in range(3)

    def valid_states(self, state: Simulator):
        return [state.deep_copy()]
