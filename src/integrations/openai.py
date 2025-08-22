
from openai import OpenAI
 
openapi_key = "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"
 

 
 
client = OpenAI(api_key=openapi_key)
 
 

def generate_plan(data):
    prompt = '''
    Your are a AI travel planer with 19 years of experience. 
    You are supposed to understand my apps user travel plan data and 
    generate a clean and simple travel plan accordingly to my user needs
    Dont wish like 'sure, i will generate etc..'
    Directly come to the point. I need only the plan.
    '''
    response = client.responses.create(
            model="gpt-4.1",
            max_output_tokens=1000,
            temperature=0.7,
            input=[
                    {
                "role": "system",
                "content": prompt
                },
                {
                    "role": "user",
                    "content": f'Please generate a travel plan for me. Details are here: {data}'
                }
            ],
        )

    return response.output_text