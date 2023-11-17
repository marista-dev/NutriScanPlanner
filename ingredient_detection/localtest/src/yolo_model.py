from ultralytics import YOLO
import os
import torch

device = torch.device("mps")

def load_and_train_model(model_path, data_path, epochs, patience, batch, imgsz, save_dir):
    # YOLO 모델 로드
    model = YOLO(model_path)

    # 모델의 클래스 이름과 개수 출력
    print(f"Model classes: {model.names}")
    print(f"Number of classes: {len(model.names)}")

    # 모델 학습
    # model.train(data = data_path, epochs = epochs, patience = patience, batch = batch, imgsz = imgsz)

    # 모델 저장 경로 확인 및 생성
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # 모델 내보내기 (예시: PyTorch 형식으로 내보내기)
    # model.export(format = 'torchscript', path = os.path.join(save_dir, 'trained_model.pt'))
    model.export(format = 'PyTorch')


if __name__ == "__main__":
    # 모델 경로, 데이터 경로 및 저장 경로 설정
    model_path = 'yolov8n.pt'
    data_path = '/Users/marista/Desktop/REPO/NutriScanPlanner/ingredient_detection/data/Ingre.yaml'
    save_dir = '../models/'

    # 모델 학습을 위한 매개변수 설정
    epochs = 10
    patience = 10
    batch = 32
    imgsz = 640

    # 모델 로드 및 학습 실행
    load_and_train_model(model_path, data_path, epochs, patience, batch, imgsz, save_dir)
