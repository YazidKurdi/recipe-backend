import openai
import dotenv
import os

from django.conf import settings

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI")

THROTTLE_RATE = int(settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES']['chef_gpt'].split('/')[0])

def get_recipe(recipe):

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system",
                   "content": "You are a professional chef who is brought to a restaurant. The restaurant has been preparing the same recipes for a while,\
                    you are tasked to change how an existing recipe is prepared. Be creative and try to create a twist on the existing recipe.\
                    Your response should be strictly a JSON object with no trailing/starting pleasantries.\
                    Format the answer as a json object with the following structure:\
                    {{  'description': content,\
                        'ingredients': content (array),\
                    }}\
                    response description format: string\
                    response ingredients format: array of objects [{name:string,unit:string,amount:string}]"
                              },
                  {"role": "user",
                   "content": f"The description is: {recipe['description']} and the ingredients are: {recipe['ingredients']}"}]
    )

    # Get the generated text from the response
    generated_text = completion.choices[0].message.content.strip()

    return generated_text
