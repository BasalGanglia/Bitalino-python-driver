import pandas as pd
import numpy as np


class BaseProcessor:
    def __init__(self) -> None:
        self.b_mean = 0
        self.b_range = 0
        self.b_counter = 0
        self.b_length = 1000
        self.base_buffer = []
        self.calibration_phase = True


class EDAProcessor(BaseProcessor):
    def __init__(self) -> None:
        super().__init__()

    def process(self, data):
        if self.calibration_phase:
            if self.b_counter < self.b_length:
                self.base_buffer.append(data)
                self.b_counter += len(data)
                if self.b_counter >= self.b_length:
                    self.calibration_phase = False
                    self.b_mean = np.mean(self.base_buffer)
                    self.b_range = np.std(self.base_buffer)
                return 0
        else:
            return (np.mean(data) - self.b_mean) / self.b_range


class PPGProcessor(BaseProcessor):
    def __init__(self) -> None:
        super().__init__()

    def process(self, data):
        if self.calibration_phase:
            if self.b_counter < self.b_length:
                self.base_buffer.append(data)
                self.b_counter += len(data)
                if self.b_counter >= self.b_length:
                    self.calibration_phase = False
                    self.b_mean = np.mean(self.base_buffer)
                    self.b_range = np.std(self.base_buffer)
                return 0
        else:
            return (np.mean(data) - self.b_mean) / self.b_range


class RespProcessor(BaseProcessor):
    def __init__(self) -> None:
        super().__init__()

    def process(self, data):
        if self.calibration_phase:
            if self.b_counter < self.b_length:
                self.base_buffer.append(data)
                self.b_counter += len(data)
                if self.b_counter >= self.b_length:
                    self.calibration_phase = False
                    self.b_mean = np.mean(self.base_buffer)
                    self.b_range = np.std(self.base_buffer)
                return 0
        else:
            return (np.mean(data) - self.b_mean) / self.b_range
