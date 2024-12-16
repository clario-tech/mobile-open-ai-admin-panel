import openai
import requests
import time
import json

open_ai_api_key = 'your_openai_api_key'
black_forest_labs_api_key = "black_forest_labs_api_key"

def create_logo(prompt, key):
    try:
        url = 'https://api.bfl.ml/v1/flux-pro-1.1-ultra'
        headers = {
            'Content-Type': 'application/json',
            'X-Key': key,
        }
        payload = {
            'prompt': prompt,
            'output_format': 'jpeg',
        }

        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        id = data.get('id')
        if not id:
            raise ValueError('ID not found in the response.')

        status = 'Pending'
        result = None
        while status != 'Ready':
            status_url = 'https://api.bfl.ml/v1/get_result'
            params = {'id': id}
            
            result_response = requests.get(status_url, headers=headers, params=params)
            result_response.raise_for_status()
            result_data = result_response.json()

            status = result_data.get('status')
            result = result_data.get('result')

            if status != 'Ready':
                print('Status not ready yet, waiting...')
                time.sleep(1)  # Wait for 2 seconds

        if result and result.get('sample'):
            print('Result ready:', result['sample'])
        else:
            print('Failed to fetch the result.')

        print('Result Response:', result_data)
    except requests.RequestException as e:
        if e.response is not None:
            print('Error:', json.dumps(e.response.json(), indent=2))
        else:
            print('Unexpected Error:', str(e))
    except Exception as ex:
        print('Unexpected Error:', str(ex))

open_ai_prompt_minimalist_prompt = """
The generated prompt should include the following:

1. The logo style must be strictly minimalist. Minimalist design emphasizes simplicity, clarity, and the use of only essential elements. It avoids clutter, unnecessary details, and complex shapes. Instead, it focuses on clean lines, balanced compositions, and limited use of colors or gradients. The design should be visually impactful while maintaining simplicity, ensuring it is easy to recognize and scalable for different applications.  
2. Preferred colors or color palettes and how they should interact, such as monochromatic schemes or subtle contrasts.  
3. Key visual elements (e.g., geometric shapes, abstract forms, or nature-inspired motifs) that align with the intended identity or purpose.  
4. Emotional tone or message the logo should convey (e.g., trust, innovation, elegance).  
5. A guideline specifying that the logo should not include any text, lettering, or the company name.  
6. Instructions to ensure the design is unique, memorable, and aligned with the intended brand identity.  

The response must not include the company name and should be delivered as plain text without any formatting. Focus on making the prompt concise yet descriptive enough to inspire creative and unique minimalist ideas. Avoid unnecessary formatting or overly technical language."""

user_input = "Yoga Studio. Sport"

client = openai.OpenAI(api_key=open_ai_api_key)

print("Creating a prompt for generating a logo...")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": open_ai_prompt_minimalist_prompt},
        {"role": "user", "content": user_input},
    ],
    temperature=1.0
)

open_ai_response = response.choices[0].message.content

create_logo(prompt=open_ai_response, key=black_forest_labs_api_key)

# print(open_ai_response)