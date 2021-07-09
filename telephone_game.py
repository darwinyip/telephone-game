from os import environ
import random

from google.cloud import translate

project_id = environ.get("PROJECT_ID", "")
assert project_id
parent = f"projects/{project_id}"
client = translate.TranslationServiceClient()

response = client.get_supported_languages(parent=parent, display_language_code="en")
language_codes = [language.language_code for language in response.languages]

user_text = input("Enter text to translate: ")

translation_rounds = 0
while translation_rounds <= 0 or translation_rounds > len(language_codes):
    translation_rounds = int(input(f"Enter number of translations (max: {len(language_codes)}): "))

selected_languages = random.sample(language_codes, translation_rounds)

current_text = user_text

print(f"Original [en]: {user_text}")

for language in selected_languages:
    response = client.translate_text(
                contents=[current_text],
                target_language_code=language,
                parent=parent,
                )

    for translation in response.translations:
            current_text = translation.translated_text
            print(f"[{language}]: {current_text}")

    response = client.translate_text(
                contents=[current_text],
                target_language_code='en',
                parent=parent,
                )

    for translation in response.translations:
            current_text = translation.translated_text
            print(f"[en]: {current_text}")
