import json
import logging
import re
import openai
import dotenv
import os

from recipe_scrapers import scrape_me


dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI")

logger = logging.getLogger("recipe_import")

predefined_cuisines = {'American, Mexican, Middle Eastern, Asian, Indian, Italian'}

class RecipeParser():

    def __init__(self, url):
        self.url = url
        self.scraper_response = scrape_me(self.url, wild_mode=True)
        self.ingredients = None
        self.title = None
        self.description = None
        self.cuisine = None

    def import_recipe(self):  ## remove
        scraper = scrape_me(self.url, wild_mode=True)
        return scraper.to_json()

    def ingredients_parse_gpt(self):
        ingredients = self.scraper_response.ingredients()
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system",
                       "content": "You are an ingredient parser assistant, your job is to parse through a list of ingredients and for each entry extract: \
                                    1. Ingredient Name \
                                    2. Ingredient Unit (You can leave this value empty if the ingredient is inherently unitless, (eg. Onion/Parsley etc..)\
                                    3. Ingredient Amount\
                                    Metric measurements are preferred to be used.\
                                    Your response should be strictly a list with no trailing/starting pleasantries.\
                                    Format your response as a list of JSON objects with the following structure:\
                                    response ingredients format: array of objects [{name:string,unit:string,amount:string}]"},
                      {"role": "user",
                       "content": f"My ingredients to be parsed are: {ingredients}"}]
        )

        return completion.choices[0].message.content.strip()


    def ingredients_cleaned(self):


        gpt_response = self.ingredients_parse_gpt()

        # Remove non-ASCII characters from the generated text
        gpt_response_ASCI = re.sub(r"[^\x20-\x7E]+", "", gpt_response)

        # Replace single quotes with double quotes in the generated text
        gpt_response_quotes = gpt_response_ASCI.replace("'", "\"")

        ingredients_list = json.loads(gpt_response_quotes)

        for obj in ingredients_list:
            if obj["amount"] == "":
                obj["amount"] = "1"

        return ingredients_list

    def recipe_json(self):

        try:

            self.ingredients = self.ingredients_cleaned()
            self.title = self.scraper_response.title()
            self.description = self.scraper_response.instructions()

            try:
                cuisine = self.scraper_response.cuisine()
                if cuisine in predefined_cuisines:
                    self.cuisine = cuisine
                else:
                    self.cuisine = "Other"
            except Exception:
                self.cuisine = "Other"

            recipe_json = {
                "title": self.title,
                "description": self.description,
                "cuisine": self.cuisine,
                "ingredients": self.ingredients
            }

            return json.dumps(recipe_json)

        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON: {e}. ingredients: {self.ingredients}")
            logger.error(f"Error decoding JSON: {e}. JSON_scraper: {self.scraper_response.to_json()}")
            raise e