from ultralytics import YOLO
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 모델 로드
model = YOLO('../models/best.pt')  # 또는 학습된 모델 경로 'path/to/trained_model.pt'

# 자신의 이미지 파일 경로로 변경
image_paths = ['egg.jpg']
# 이미지에 대한 추론 수행
results = model(image_paths)

# 결과 출력 및 시각화
for result in results:
    print("Detected objects:")
    # 경계 상자 정보 추출
    if len(result.boxes.xyxy) > 0:
        box = result.boxes.xyxy[0]
        if box.numel() == 4:  # 박스에 4개의 요소가 있는지 확인
            x1, y1, x2, y2 = box
            fig, ax = plt.subplots(1, figsize=(8, 8))
            ax.imshow(result.orig_img)
            rect = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            plt.show()
        else:
            print("Unexpected box format:", box)
    else:
        print("  No objects detected.")