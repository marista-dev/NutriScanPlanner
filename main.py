import gradio as gr
from ingredient_detection.ingredient_detection_module import create_ingredient_detection_interface
from tdee_calculator.tdee_module import create_tdee_calculator_interface
from diet_planner.diet_planner_module import create_diet_planner_interface
import openai
from openai import OpenAI

# OpenAI 라이브러리에 API 키 설정
openai.api_key = ''
client = OpenAI(api_key='')

"""
def answer(state, text):
    
    if not state:
        state = [{"role": "system", "content": "You are a helpful assistant."}]

    # 대화 기록에 사용자의 메시지 추가
    state.append({"role": "user", "content": text})

    # OpenAI에 요청을 보냄
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=state
    )

    # OpenAI로부터 받은 응답의 내용을 추가
    assistant_message_content = response.choices[0].message.content
    assistant_message = {"role": "assistant", "content": assistant_message_content}
    state.append(assistant_message)

    # 채팅 인터페이스에 표시될 응답 메시지
    display_message = assistant_message_content

    return state, display_message

"""
# answer 함수 정의
def answer(chat_history, user_input):
    if not chat_history:
        chat_history = [["system", "You are a helpful assistant."]]

    chat_history.append(["user", user_input])

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        # model="gpt-4",
        messages=[{"role": role, "content": content} for role, content in chat_history]
    )
    assistant_reply = response.choices[0].message.content
    chatbot_history = [[user_input, assistant_reply]]
    chat_history.append(["user", assistant_reply])

    return gr.Chatbot(value = chatbot_history)

# 각 모듈의 인터페이스 생성 함수를 호출
ingredient_demo, predict, handle_selection = create_ingredient_detection_interface()
tdee_demo, calculate_calories_mifflin_st_jeor, handle_calorie_selection = create_tdee_calculator_interface()
diet_planner_demo, translate_text_with_deepl, generate_diet_plan = create_diet_planner_interface()

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column(scale = 1):
            gr.Markdown("## Object Detection with Roboflow")
            image_input = gr.Image(type="pil", label="Upload Image")
            confidence_slider = gr.Slider(minimum=0, maximum=100, value=40, label="Confidence Threshold")
            overlap_slider = gr.Slider(minimum=0, maximum=100, value=30, label="Overlap Threshold")
            predict_button = gr.Button("Predict")
            ingredients_checkbox_group = gr.CheckboxGroup(label="Select Ingredients")
            selection_output = gr.Textbox()

            predict_button.click(
                fn=predict,  # 수정된 함수 참조
                inputs=[image_input, confidence_slider, overlap_slider],
                outputs=ingredients_checkbox_group
            )

            ingredients_checkbox_group.change(
                fn=handle_selection,  # 수정된 함수 참조
                inputs=ingredients_checkbox_group,
                outputs=selection_output
            )

        with gr.Column(scale = 1):
            gr.Markdown("## TDEE 계산기")
            gender_input = gr.Radio(label="Gender", choices=["Male", "Female"])
            age_input = gr.Number(label="Age (years)")
            height_input = gr.Number(label="Height (cm)")
            weight_input = gr.Number(label="Weight (kg)")
            activity_level_input = gr.Dropdown(
                label="Activity Level",
                choices=[
                    "Sedentary (office job)",
                    "Light Exercise (1-2 days/week)",
                    "Moderate Exercise (3-5 days/week)",
                    "Heavy Exercise (6-7 days/week)"
                ]
            )

            calculate_button = gr.Button("Calculate")
            calories_output = gr.CheckboxGroup(label = "Calorie Option")
            calories_selection_output = gr.Textbox()

            calculate_button.click(
                fn = calculate_calories_mifflin_st_jeor,
                inputs = [gender_input, age_input, height_input, weight_input, activity_level_input],
                outputs = calories_output
            )
            calories_output.change(
                fn = handle_calorie_selection,
                inputs = calories_output,
                outputs = calories_selection_output
            )
        with gr.Column(scale = 2):
            gr.Markdown("## 식단 계획 결과")
            result = gr.Markdown()
        with gr.Row():
            with gr.Column(scale = 2):
                # Diet Planner 모듈의 구성 요소 추가
                gr.Markdown("## 식단 구성")
                # Diet Planner 모듈의 나머지 입력 컴포넌트 구성
                ingredients = selection_output
                calories = calories_selection_output
                cuisine = gr.CheckboxGroup(choices = ["한식", "중식", "양식"], label = "카테고리")
                dietary_restrictions = gr.CheckboxGroup(choices = ["채식", "저탄수화물"], label = "식이 제한")
                allergies = gr.CheckboxGroup(choices = ["땅콩", "우유", "글루텐"], label = "알레르기 및 불내성")
                medical_conditions = gr.CheckboxGroup(choices = ["당뇨병", "고혈압"], label = "의료 상태")
                meals_per_day = gr.Radio(choices = ["2끼", "3끼", "4끼"], label = "하루 몇 끼 섭취")
                cooking_preference = gr.CheckboxGroup(choices = ["간단한 조리", "긴 조리 시간"], label = "조리 시간 및 용이성")
                submit_button = gr.Button("식단 생성")


                submit_button.click(
                    generate_diet_plan,
                    inputs = [ingredients, calories, cuisine,
                              dietary_restrictions, allergies, medical_conditions, meals_per_day, cooking_preference],
                    outputs = result
                )
            with gr.Column(scale = 1):
                # state = gr.State()
                # chat_input = gr.Textbox(show_label = False, placeholder = 'Send a message...')
                # chat_output = gr.Markdown()
                # submit_button = gr.Button("Send")
                #
                # submit_button.click(
                #     fn = answer,
                #     inputs = [state, chat_input],
                #     outputs = [state, chat_output]
                # )
                # ChatInterface 추가
                gr.Markdown("## GPT 채팅")
                chat_history = gr.State()
                chat_output = gr.Chatbot()
                chat_input = gr.Textbox(show_label = False, placeholder = "메시지를 입력하세요...")
                submit_button = gr.Button("전송")



                # # answer 함수 정의
                # def answer(chat_history, user_input):
                #     if not chat_history:
                #         chat_history = [("system", "You are a helpful assistant.")]
                #
                #     # 사용자 입력을 튜플 형식으로 채팅 기록에 추가
                #     chat_history.append(("user", user_input))
                #
                #     # OpenAI GPT 모델에 채팅 기록 전송 및 응답 받기
                #     response = client.chat.completions.create(
                #         model = "gpt-3.5-turbo",
                #         messages = [{"role": role, "content": content} for role, content in chat_history]
                #     )
                #
                #     # 모델의 응답을 튜플 형식으로 채팅 기록에 추가
                #     assistant_reply = response.choices[0].message.content
                #     chat_history.append(("assistant", assistant_reply))
                #
                #     # 빈 문자열과 채팅 기록을 반환
                #     return "", chat_history


                submit_button.click(
                    fn = answer,
                    inputs = [chat_history, chat_input],
                    outputs = chat_output
                )

# Blocks 인터페이스와 ChatInterface 실행
demo.launch(debug = True)
