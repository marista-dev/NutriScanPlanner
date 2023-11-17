import gradio as gr
from ultralytics import YOLO
import PIL.Image as Image
import io
import json

# 모델 로드 (상대 경로 사용)
model_path = '../models/best.pt'
model = YOLO(model_path)
print(f"Model classes: {model.names}")
print(f"Number of classes: {len(model.names)}")

# 객체 감지 함수 정의
def detection(image, threshold):
    model.overrides['conf'] = threshold  # 객체 신뢰도 임계값 설정
    results = model.predict([image], stream = False)

    result = results[0]
    detected_items = []

    # 결과를 JSON 형식으로 변환
    json_results = json.loads(result.tojson())
    for detection in json_results:
        class_name = detection['class']
        detected_items.append(class_name)

    detected_str = ', '.join(detected_items) if detected_items else "No items detected"

    # 결과 이미지에 탐지 결과 플롯
    plotted_image = Image.fromarray(result.plot())

    return plotted_image, detected_str


# Gradio 인터페이스 구성
with gr.Blocks() as demo:
    with gr.Tab("Detection"):
        with gr.Row():
            with gr.Column():
                detect_input = gr.Image()
                detect_threshold = gr.Slider(maximum = 1, step = 0.01, value = 0.25, label = "Threshold:",
                                             interactive = True)
                detect_button = gr.Button("Detect!")
            with gr.Column():
                detect_output_image = gr.Image(label = "Predictions:", interactive = False)
                detect_output_text = gr.Textbox(label = "Detected Items:")

    detect_button.click(
        detection,
        inputs = [detect_input, detect_threshold],
        outputs = [detect_output_image, detect_output_text]
    )

# 인터페이스 실행
demo.launch()
