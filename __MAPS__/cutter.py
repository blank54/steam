import numpy as np
from mid_uav import MAP

# 주어진 MAP 데이터를 numpy 배열로 변환
MAP = np.array(MAP)

# 원하는 10x10 부분을 추출 (예: 좌상단에서 시작)
start_row, start_col = 5, 5  # 시작 위치 조정 가능
sub_map = MAP[start_row:start_row+40, start_col:start_col+40]

# Python 리스트로 변환
sub_map_list = sub_map.tolist()

# Python 파일로 저장
file_name = "{MAP}_200.py"
with open(file_name, "w", encoding="utf-8") as file:
    file.write(f"sub_map = {sub_map_list}")

print(f"10x10 부분 맵이 '{file_name}' 파일로 저장되었습니다.")
