import os, sys, time, importlib, json, copy
from datetime import datetime
import numpy as np
from cpuinfo import get_cpu_info
from _PlotTools import VisualTool
from HarrisCorner.HCD_tools import *
from SensorModule import Sensor
from SensorModule.coverage import *

# 사용할 알고리즘
from Algorithm.GeneticAlgorithm import *


class SensorDeployment:
    def __init__(self, map_name, coverage, generation):
        self.visual_module = VisualTool()
        self.map_name = map_name
        self.coverage = coverage/5
        self.GEN = generation
        map_module_path = f"__MAPS__.{map_name}"
        map_module = importlib.import_module(map_module_path)
        self.MAP = np.array(getattr(map_module, "MAP"))

    @staticmethod
    def record_metadata(runtime, num_sensor, coverage_score, sensor_positions, map_name="Unknown", output_dir="__RESULTS__"):
        os.makedirs(output_dir, exist_ok=True)
        now = datetime.now()
        time_str = now.strftime("%m-%d_%H-%M-%S")
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        file_name = f"result_{time_str}.json"
        output_file = os.path.join(output_dir, file_name)
        cpu_info = get_cpu_info()['brand_raw']
        
        if not isinstance(sensor_positions, list):
            sensor_positions = []
        sensor_positions = [(int(pos[0]), int(pos[1])) for pos in sensor_positions]
        
        metadata = {
            "Timestamp": current_time,
            "CPU Name": cpu_info,
            "Runtime (s)": float(runtime),
            "Map Name": map_name,
            "Total Sensors": int(num_sensor),
            "Coverage Ratio" : float(coverage_score),
            "Sensor Positions": sensor_positions
        }
        with open(output_file, mode='w', encoding='utf-8') as file:
            json.dump(metadata, file, ensure_ascii=False, indent=4)
        print(f"Result save at : {output_file}")


    #최외곽 지점 센서 배치 메서드
    def corner_deploy(self, map):
        layer_corner = copy.deepcopy(map)
        corner_instance = HarrisCorner(layer_corner)
        points_corner = corner_instance.run(
                                    map=layer_corner,
                                    block_size=3,
                                    ksize=3,
                                    k=0.05,
                                    dilate_size=5
                                )
        
        if not isinstance(points_corner, list):
            points_corner = []
        else:
            for pos in points_corner:
                layer_corner[pos[1], pos[0]] = 10
                
        return layer_corner, points_corner


    #내부 지점 센서 배치 메서드
    def inner_sensor_deploy(self, map, experiment_dir):
        layer_inner = copy.deepcopy(map)
        inner_layer, inner_points, coverage_score = SensorGA(layer_inner, self.coverage, self.GEN, results_dir=experiment_dir).run()
        if not isinstance(inner_points, list):
            inner_points = []
        for pos in inner_points:
            layer_inner[pos[1], pos[0]] = 10
        return layer_inner, inner_points, coverage_score


    #인스턴스 동작 메서드
    def run(self):
        start_time = time.time()
        now = datetime.now().strftime("%m-%d-%H-%M-%S")
        experiment_dir = os.path.join("__RESULTS__", now)
        os.makedirs(experiment_dir, exist_ok=True)

        #1. 최외곽 센서 배치
        layer_corner, points_corner = self.corner_deploy(self.MAP)
        self.visual_module.showJetMap_circle(
            "Corner Sensor Deployment", layer_corner, self.coverage, points_corner,
            save_path=os.path.join(experiment_dir, "corner_sensor_result")
        )

        #2.1. 내부 센서 최적화 배치
        layer_result, inner_points, coverage_score = self.inner_sensor_deploy(layer_corner, experiment_dir)
        if not isinstance(points_corner, list):
            points_corner = []
        if not isinstance(inner_points, list):
            inner_points = []

        
        
        #3. 최종 센서 배치 결과
        total_sensors = len(points_corner) + len(inner_points)
        runtime = time.time() - start_time
        all_sensor_positions = points_corner + inner_points
        
        #3.2. 커버리지 비율 계산
        uncover_area = Sensor(self.MAP)
        uncovered = uncover_area.deploy(all_sensor_positions, self.coverage)
        uncovered_score = np.sum(uncovered == 2)
        total_site = np.sum(self.MAP == 1)
        print("전체영역(1)", total_site)
        print("미커버영역", uncovered_score)
        coverage_score = ((total_site - uncovered_score) / total_site)*100
        print("Coverage Ratio", coverage_score)
        
        self.visual_module.showJetMap_circle(
            "Final Sensor Deployment", layer_result, self.coverage, all_sensor_positions,
            save_path=os.path.join(experiment_dir, "Final_sensor_result")
        )
        self.save_checkpoint_folder = experiment_dir
        self.record_metadata(runtime, total_sensors, coverage_score, all_sensor_positions, self.map_name, output_dir=experiment_dir)
        
    #4. 수동배치 시 사용
    #all_sensor_positions = [[2,11],[21,2],[14,17],[37,12],[34,6],[16,43]]
    def manual_deploy(self, sensor_positions, experiment_dir=   "__RESULTS__"):
        all_sensor_positions = sensor_positions
        self.visual_module.showJetMap("Site Map", self.MAP, save_path=experiment_dir)
        self.visual_module.showJetMap_circle(
            "Manual Sensor Deployment", self.MAP, self.coverage, all_sensor_positions,
            save_path=os.path.join(experiment_dir, "Manual_sensor_result")
        )         
                                

# 코드 본체
if __name__ == "__main__":
    #100x100 Map 실행
    for i in range(1):
        map_name = "map_100x100.top"
        instance = SensorDeployment(map_name, 45, 10)
        instance.visual_module.showJetMap("Original Map", instance.MAP, filename="original_map")
        instance.run()
    for i in range(1):
        map_name = "map_100x100.mid"
        instance = SensorDeployment(map_name, 45, 100)
        instance.visual_module.showJetMap("Original Map", instance.MAP, filename="original_map")
        instance.run()
    for i in range(1):
        map_name = "map_100x100.bot"
        instance = SensorDeployment(map_name, 45, 100)
        instance.visual_module.showJetMap("Original Map", instance.MAP, filename="original_map")
        instance.run()
        
    #200x200 Map 실행    
    for i in range(1):
        map_name = "map_200x200.top"
        instance = SensorDeployment(map_name, 45, 100)
        instance.visual_module.showJetMap("Original Map", instance.MAP, filename="original_map")
        instance.run()
    for i in range(1):
        map_name = "map_200x200.mid"
        instance = SensorDeployment(map_name, 45, 100)
        instance.visual_module.showJetMap("Original Map", instance.MAP, filename="original_map")
        instance.run()
    for i in range(1):
        map_name = "map_200x200.bot"
        instance = SensorDeployment(map_name, 45, 100)
        instance.visual_module.showJetMap("Original Map", instance.MAP, filename="original_map")
        instance.run()
    
    #250x280 Map 실행
    for i in range(1):
        map_name = "map_250x280.top"
        instance = SensorDeployment(map_name, 45, 100)
        instance.visual_module.showJetMap("Original Map", instance.MAP, filename="original_map")
        instance.run()
    for i in range(1):
        map_name = "map_250x280.mid"
        instance = SensorDeployment(map_name, 45, 100)
        instance.visual_module.showJetMap("Original Map", instance.MAP, filename="original_map")
        instance.run()
    for i in range(1):
        map_name = "map_250x280.bot"
        instance = SensorDeployment(map_name, 45, 100)
        instance.visual_module.showJetMap("Original Map", instance.MAP, filename="original_map")
        instance.run()
        
    #570x1100 Map 실행    
    for i in range(1):
        map_name = "map_570x1100.large"
        instance = SensorDeployment(map_name, 45, 500)
        instance.visual_module.showJetMap("Original Map", instance.MAP, filename="original_map")
        instance.run()
        
    
