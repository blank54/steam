# 1. 가벼운 Python 공식 이미지 사용 (Slim 버전)
FROM python:3.11-slim
# Dockerfile for Python Development Environment with OpenCV

# 2. 작업 디렉토리 설정
WORKDIR /workspace

# 3. 필수 시스템 패키지 설치 (OpenCV 등 그래픽 라이브러리 지원)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 4. 로컬 파일을 컨테이너로 복사
COPY . /workspace

# 5. pip 최신 버전으로 업그레이드 후 라이브러리 설치 (캐시 제거)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. 개발 환경 유지 (bash로 대기)
CMD ["sh", "-c", "cd /workspace && bash"]

