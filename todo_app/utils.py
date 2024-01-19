# todo_app/utils.py
import openai

def generate_openai_response(input):
    openai.api_key = ''
    prompt = f"Generate steps for completing the input task {input}, complete it in 200 words:"
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Replace with the correct engine name
        prompt=prompt,
        max_tokens=300
    )
    steps = response.choices[0].text.strip().split('\n')
    formatted_response = '\n'.join(steps)
    return formatted_response
