import os, sys
import numpy as np
import time
from itertools import combinations
from Sensor_GPU import *


class sensor_greedy:
    def __init__(self, MAP:list, coverage:int):
        self.map = np.array(MAP)
        self.coverage = coverage
    
    #센서가 안깔린 구역의 좌표 추출
    def non_cover(self, data):
        cord_list = []
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if (data[i][j] == 1):
                    cord_list.append((j+1,i+1))
        return cord_list


    #모든 구역에 센서를 커버
    def fill_sensor(self, map_input):
        cord_list = self.non_cover(map_input)
        sensor_instance = Sensor(map_input)
        for i in cord_list:
            sensor_instance.deploy(i, self.coverage)
        return sensor_instance.result()

    
    #센서가 모든 구역을 커버하는지 판단
    def is_full(self, data):
        true = 0 #yes
        false = 0 #no
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if self.map[i][j] == 1:    
                    if (self.map[i][j] // 10) != 0:
                        true += 1
                    else:
                        false += 1
        if false > 0:
            return False
        else:
            return True

    
    def run(self):
        start = time.time()
        cord = []
        full_map = self.fill_sensor(self.map)
        non_cord = self.non_cover(self.map)
        
        s = Sensor(full_map)
        for i in non_cord:
            print("running...")
            s.retrieve(i, self.coverage)
            if self.is_full(full_map) == True:
                pass
            else:
                print(self.is_full(full_map))
                cord.append(i)

 
        print(f"Runtime : {time.time()-start:.4f}sec")
        return cord
    
    
    
    def return_map(self):
        return self.map