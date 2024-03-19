import serial_backend
from scipy import linalg
import numpy as np
calibration_state = 0

mag_bias = np.zeros([3, 1])
mag_matrix = np.eye(3)
mean_resolution = 0

class Magnetometer(object):
    MField = 300

    def __init__(self, F=MField):

        # initialize values
        self.F = F
        self.b = np.zeros([3, 1])
        self.A_1 = np.eye(3)

    def run(self):
        global mag_bias, mag_matrix, mean_resolution
        combined_mag_data = [serial_backend.mag_x_raw, serial_backend.mag_y_raw, serial_backend.mag_z_raw]
        s = np.array(combined_mag_data)

        M, n, d = self.__ellipsoid_fit(s)

        # calibration parameters
        M_1 = linalg.inv(M)
        self.b = -np.dot(M_1, n)

        data_no_bias = s - self.b
        data_no_bias = np.abs(data_no_bias)
        mean_resolution = np.mean(data_no_bias)

        # self.A_1 = np.real(self.F / np.sqrt(np.dot(n.T, np.dot(M_1, n)) - d) * linalg.sqrtm(M))
        self.A_1 = np.real((mean_resolution*2) / np.sqrt(np.dot(n.T, np.dot(M_1, n)) - d) * linalg.sqrtm(M))

        mag_bias = self.b
        mag_matrix = self.A_1

    def __ellipsoid_fit(self, s):

        D = np.array([s[0] ** 2., s[1] ** 2., s[2] ** 2.,
                      2. * s[1] * s[2], 2. * s[0] * s[2], 2. * s[0] * s[1],
                      2. * s[0], 2. * s[1], 2. * s[2], np.ones_like(s[0])])

        # S, S_11, S_12, S_21, S_22 (eq. 11)
        S = np.dot(D, D.T)
        S_11 = S[:6, :6]
        S_12 = S[:6, 6:]
        S_21 = S[6:, :6]
        S_22 = S[6:, 6:]

        # C (Eq. 8, k=4)
        C = np.array([[-1, 1, 1, 0, 0, 0],
                      [1, -1, 1, 0, 0, 0],
                      [1, 1, -1, 0, 0, 0],
                      [0, 0, 0, -4, 0, 0],
                      [0, 0, 0, 0, -4, 0],
                      [0, 0, 0, 0, 0, -4]])

        # v_1 (eq. 15, solution)
        E = np.dot(linalg.inv(C),
                   S_11 - np.dot(S_12, np.dot(linalg.inv(S_22), S_21)))

        E_w, E_v = np.linalg.eig(E)

        v_1 = E_v[:, np.argmax(E_w)]
        if v_1[0] < 0: v_1 = -v_1

        # v_2 (eq. 13, solution)
        v_2 = np.dot(np.dot(-np.linalg.inv(S_22), S_21), v_1)

        # quadratic-form parameters, parameters h and f swapped as per correction by Roger R on Teslabs page
        M = np.array([[v_1[0], v_1[5], v_1[4]],
                      [v_1[5], v_1[1], v_1[3]],
                      [v_1[4], v_1[3], v_1[2]]])
        n = np.array([[v_2[0]],
                      [v_2[1]],
                      [v_2[2]]])
        d = v_2[3]

        return M, n, d

