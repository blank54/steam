import numpy as np
import matplotlib.pyplot as plt
from numba import njit, prange

class Sensor:
    def __init__(self, MAP):
        self.map_data = np.array(MAP)  # 원본 맵 데이터 저장
        self.width = self.map_data.shape[1]
        self.height = self.map_data.shape[0]

    def deploy(self, sensor_positions, coverage_radius):
        """
        센서를 배치하여 커버리지를 적용
        :param sensor_positions: 센서 좌표 리스트 ([(x1, y1), (x2, y2), ...])
        :param coverage_radius: 센서 커버 반경
        """
        sensor_positions = np.array(sensor_positions, dtype=np.int32)  # 🚀 리스트를 NumPy 배열로 변환

        # 커버리지 적용
        coverage_map = np.zeros_like(self.map_data)
        apply_coverage(coverage_map, sensor_positions, coverage_radius, self.width, self.height)

        #미커버 영역 찾기 (설치 가능한 곳(MAP == 1) 중에서 센서가 커버하지 못한 곳(coverage_map == 0))
        uncovered_map = np.where((self.map_data == 1) & (coverage_map == 0), 2, self.map_data)  # 2: 미커버 영역 표시

        return uncovered_map  # 2가 미커버 영역

from numba import njit

@njit  
def apply_coverage(coverage_map, sensor_positions, radius, width, height):
    for i in range(sensor_positions.shape[0]):  # prange -> range
        x, y = sensor_positions[i]
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height and abs(dx) + abs(dy) <= radius:
                    coverage_map[ny, nx] = 1

