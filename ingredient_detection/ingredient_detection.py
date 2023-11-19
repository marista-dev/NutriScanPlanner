import gradio as gr
from roboflow import Roboflow
import PIL.Image as Image

# Roboflow API 키와 프로젝트 설정
api_key = ""
rf = Roboflow(api_key=api_key)
project = rf.workspace().project("ingredients_yolo")
model = project.version(3).model

# 이미지에 대한 예측을 수행하는 함수
def predict(image, confidence, overlap):
    temp_file_path = "temp_image.jpg"
    image.save(temp_file_path)
    result = model.predict(temp_file_path, confidence=confidence, overlap=overlap)
    predictions = result.json()["predictions"]
    detected_classes = [pred["class"] for pred in predictions]
    unique_classes = list(set(detected_classes))  # 중복 제거
    return gr.CheckboxGroup(choices = unique_classes)

# 사용자가 CheckboxGroup에서 선택한 항목을 처리하는 함수
def handle_selection(selected_items):
    # 여기에 선택된 항목을 처리하는 로직을 구현
    return ", ".join(selected_items)

# Gradio Blocks 인터페이스 구성
with gr.Blocks() as demo:
    gr.Markdown("## Object Detection with Roboflow")
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload Image")
            confidence_slider = gr.Slider(minimum=0, maximum=100, value=40, label="Confidence Threshold")
            overlap_slider = gr.Slider(minimum=0, maximum=100, value=30, label="Overlap Threshold")
            predict_button = gr.Button("Predict")
        with gr.Column():
            ingredients_checkbox_group = gr.CheckboxGroup(label="Select Ingredients")
            selection_output = gr.Textbox()  # 선택된 항목을 표시할 레이블

    # 'Predict' 버튼 클릭 시 동작 정의
    predict_button.click(
        fn=predict,
        inputs=[image_input, confidence_slider, overlap_slider],
        outputs=ingredients_checkbox_group
    )

    # CheckboxGroup에서 선택 변경 시 동작 정의
    ingredients_checkbox_group.change(
        fn=handle_selection,
        inputs=ingredients_checkbox_group,
        outputs=selection_output
    )
demo.launch()
# return demo
#
# # 인터페이스 생성
# ingredient_detection_interface = ingredient_detection_interface()