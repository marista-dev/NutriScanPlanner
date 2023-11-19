import gradio as gr

def calculate_calories_mifflin_st_jeor(gender, age, height, weight, activity_level):
    # Mifflin-St Jeor Equation for BMR
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:  # Female
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 151

    # Activity level multipliers
    activity_multipliers = {
        "Sedentary (office job)": 1.2,
        "Light Exercise (1-2 days/week)": 1.375,
        "Moderate Exercise (3-5 days/week)": 1.55,
        "Heavy Exercise (6-7 days/week)": 1.725
    }
    activity_multiplier = activity_multipliers[activity_level]

    # Adjust BMR based on activity level to get Total Daily Energy Expenditure (TDEE)
    tdee = bmr * activity_multiplier

    # Calculating calories for weight loss, maintenance, and bulking, then round the results
    weight_loss_calories = round(tdee - 500)  # Subtract 500 calories for weight loss
    maintenance_calories = round(tdee)        # Maintenance
    bulkup_calories = round(tdee + 500)       # Add 500 calories for bulking up
    calories_classes = [
        ("Weight Loss Calories", f"{weight_loss_calories} kcal - 체중 감량용"),
        ("Maintenance Calories", f"{maintenance_calories} kcal - 체중 유지용"),
        ("Bulking Up Calories", f"{bulkup_calories} kcal - 근육 증가용")
    ]
    return gr.CheckboxGroup(choices = calories_classes)
    # return weight_loss_calories, maintenance_calories, bulkup_calories
# 선택된 칼로리 옵션을 처리하는 함수
def handle_calorie_selection(selected_items):
    return ", ".join(selected_items)

# Gradio Blocks 인터페이스 정의 함수
def create_tdee_calculator_interface():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
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
                calories_output = gr.Textbox()

                calculate_button.click(
                    fn=calculate_calories_mifflin_st_jeor,
                    inputs=[gender_input, age_input, height_input, weight_input, activity_level_input],
                    outputs=calories_output
                )
    return demo, calculate_calories_mifflin_st_jeor, handle_calorie_selection

# 인터페이스 생성 함수 호출
tdee_calculator_interface = create_tdee_calculator_interface()
