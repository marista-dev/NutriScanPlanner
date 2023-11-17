# 각 모듈 임포트
from ingredient_detection import ingredient_detection
from tdee_calculator import tdee
from diet_planner import diet_planner
from gpt_chat import chat_gpt

import gradio as gr

# 각 기능에 대한 Gradio 인터페이스 정의
ingredient_detection_interface = gr.Interface(...)
tdee_calculator_interface = gr.Interface(...)
diet_planner_interface = gr.Interface(...)
gpt_chat_interface = gr.Interface(...)

# 모든 인터페이스를 탭 인터페이스로 통합
tabbed_interface = gr.TabbedInterface(
    interface_list=[
        ingredient_detection_interface,
        tdee_calculator_interface,
        diet_planner_interface,
        gpt_chat_interface
    ],
    tab_names=["식재료 디텍팅", "TDEE 계산기", "식단 생성", "GPT 채팅"]
)

# 탭 인터페이스 실행
tabbed_interface.launch()
