import gradio as gr
from roboflow import Roboflow
import PIL.Image as Image

def create_ingredient_detection_interface():
    # Roboflow API 키와 프로젝트 설정
    api_key = "glpg6nG8bAL9f2I1sKoP"
    rf = Roboflow(api_key=api_key)
    project = rf.workspace().project("foodingredientsdetection-nk3my")
    model = project.version(10).model


    # 이미지에 대한 예측을 수행하는 함수
    def predict(image, confidence, overlap):
        temp_file_path = "temp_image.jpg"
        image.save(temp_file_path)
        result = model.predict(temp_file_path, confidence=confidence, overlap=overlap)
        predictions = result.json()["predictions"]
        detected_classes = [pred["class"] for pred in predictions]
        unique_classes = list(set(detected_classes))
        return gr.CheckboxGroup(choices = unique_classes)

    # 사용자가 CheckboxGroup에서 선택한 항목을 처리하는 함수
    def handle_selection(selected_items):
        return ", ".join(selected_items)

    # Gradio Blocks 인터페이스 정의
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                gr.Markdown("## Object Detection with Roboflow")
                image_input = gr.Image(type="pil", label="Upload Image")
                confidence_slider = gr.Slider(minimum=0, maximum=100, value=40, label="Confidence Threshold")
                overlap_slider = gr.Slider(minimum=0, maximum=100, value=30, label="Overlap Threshold")
                predict_button = gr.Button("Predict")
                ingredients_checkbox_group = gr.CheckboxGroup(label="Select Ingredients")
                ingredient_selection_output = gr.Textbox()

                predict_button.click(
                    fn=predict,
                    inputs=[image_input, confidence_slider, overlap_slider],
                    outputs=ingredients_checkbox_group
                )

                ingredients_checkbox_group.change(
                    fn=handle_selection,
                    inputs=ingredients_checkbox_group,
                    outputs=ingredient_selection_output
                )

    return demo, predict, handle_selection

# 인터페이스 생성 함수 호출
ingredient_detection_interface = create_ingredient_detection_interface()
