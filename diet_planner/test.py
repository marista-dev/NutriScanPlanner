import gradio as gr
import openai
import deepl
from openai import OpenAI

# OpenAI 및 DeepL API 키 설정
openai.api_key = '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'
client = OpenAI(api_key='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')

auth_key = "6309462f-ad40-dba2-f27f-e297c462fcd9:fx"  # 여기에 DeepL 인증 키 입력
translator = deepl.Translator(auth_key)

def translate_text_with_deepl(text, target_language="KO"):
    try:
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as error:
        print(error)
        return text  # 번역 실패 시 원문 반환

def generate_diet_plan(calories, ingredients, cuisine, dietary_restrictions, allergies, medical_conditions, meals_per_day, cooking_preference):
    # 구조화된 형식으로 채팅 메시지 생성
    messages = [
        {"role": "system", "content": "You are an assistant capable of creating personalized diet plans."},
        {"role": "user", "content": f"Create a diet plan with the following requirements in a structured format easy to parse:\nCalories: {calories}\nIngredients: {ingredients}\nCuisine: {cuisine}\nDietary Restrictions: {dietary_restrictions}\nAllergies: {allergies}\nMedical Conditions: {medical_conditions}\nMeals per day: {meals_per_day}\nCooking Preference: {cooking_preference}\n\nPlease format each meal as follows:\nMeal Type: [Meal type], Contents: [Meal contents], Calories: [Calorie count]"}
    ]

    # GPT-3 API 호출
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # 결과를 마크다운 형식으로 변환
    diet_plan = completion.choices[0].message.content
    markdown_format = format_diet_plan_as_markdown(diet_plan)

    return markdown_format

def format_diet_plan_as_markdown(diet_plan):
    lines = diet_plan.split('\n')
    markdown_table = "구분 | 식단 | 칼로리\n--- | --- | ---\n"

    meal_type = ""
    meal_content = ""
    calories = ""

    for line in lines:
        if "Meal Type:" in line:
            meal_type = line.split("Meal Type:")[1].strip()
        elif "Contents:" in line:
            meal_content = line.split("Contents:")[1].strip()
        elif "Calories:" in line:
            calories = line.split("Calories:")[1].strip()
            # 마크다운 테이블에 행 추가
            markdown_table += f"{meal_type} | {meal_content} | {calories}\n"

    return markdown_table


    # 결과 추출 및 번역
    diet_plan = completion.choices[0].message.content
    translated_diet_plan = translate_text_with_deepl(diet_plan, "KO")  # 한국어로 번역
    markdown_format = format_diet_plan_as_markdown(translated_diet_plan)

    return markdown_format


# Gradio 인터페이스 구성
with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            # 인풋 구성
            calories = gr.Number(label="TDEE 계산기로 입력받은 칼로리")
            ingredients = gr.Textbox(label="식재료")
            cuisine = gr.CheckboxGroup(choices=["한식", "중식", "양식"], label="카테고리")
            dietary_restrictions = gr.CheckboxGroup(choices=["채식", "저탄수화물"], label="식이 제한")
            allergies = gr.CheckboxGroup(choices=["땅콩", "우유", "글루텐"], label="알레르기 및 불내성")
            medical_conditions = gr.CheckboxGroup(choices=["당뇨병", "고혈압"], label="의료 상태")
            meals_per_day = gr.Radio(choices=["2끼", "3끼", "4끼"], label="하루 몇 끼 섭취")
            cooking_preference = gr.CheckboxGroup(choices=["간단한 조리", "긴 조리 시간"], label="조리 시간 및 용이성")
            submit_button = gr.Button("식단 생성")

        with gr.Column():
            # 결과 출력
            result = gr.Markdown()

    # 버튼 클릭 시 동작 정의
    submit_button.click(
        generate_diet_plan,
        inputs=[calories, ingredients, cuisine, dietary_restrictions, allergies, medical_conditions, meals_per_day, cooking_preference],
        outputs=result
    )

demo.launch()
