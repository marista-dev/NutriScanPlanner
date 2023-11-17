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

    return weight_loss_calories, maintenance_calories, bulkup_calories

# Gradio Interface
interface = gr.Interface(
    fn=calculate_calories_mifflin_st_jeor,
    inputs=[
        gr.Radio(label="Gender", choices=["Male", "Female"]),
        gr.Number(label="Age (years)"),
        gr.Number(label="Height (cm)"),
        gr.Number(label="Weight (kg)"),
        gr.Dropdown(
            label="Activity Level",
            choices=[
                "Sedentary (office job)",
                "Light Exercise (1-2 days/week)",
                "Moderate Exercise (3-5 days/week)",
                "Heavy Exercise (6-7 days/week)"
            ]
        )
    ],
    outputs=[
        gr.Textbox(label="Calories for Weight Loss"),
        gr.Textbox(label="Calories for Maintenance"),
        gr.Textbox(label="Calories for Bulking Up")
    ],
    title="Daily Calorie Calculator using Mifflin-St Jeor Formula",
    description="Calculate your daily calorie needs for weight loss, maintenance, and bulking up based on your gender, age, height, weight, and activity level using the Mifflin-St Jeor Formula."
)

# Run the interface
interface.launch()
