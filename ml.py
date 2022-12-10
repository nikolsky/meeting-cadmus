# Imports the Google Cloud Translation library
import six
from google.cloud import translate_v2 as translate

import os
import openai
openai.organization = "org-JaGJq15JH1OngBfov966SFaN"
openai.api_key = os.getenv("OPENAI_API_KEY")

PROJECT_ID = "my-project-98575-371210"

## Initialize Translation client
#def translate_text(text="YOUR_TEXT_TO_TRANSLATE", project_id="YOUR_PROJECT_ID"):
#    """Translating Text."""
#
#    client = translate.TranslationServiceClient()
#
#    location = "global"
#
#    parent = f"projects/{project_id}/locations/{location}"
#
#    # Translate text from English to French
#    # Detail on supported types can be found here:
#    # https://cloud.google.com/translate/docs/supported-formats
#    response = client.translate_text(
#        request={
#            "parent": parent,
#            "contents": [text],
#            "mime_type": "text/plain",  # mime types: text/plain, text/html
#            "source_language_code": "ru-RU",
#            "target_language_code": "en-US",
#        }
#    )
#
#    # Display the translation for each input text provided
#    for translation in response.translations:
#        print("Translated text: {}".format(translation.translated_text))

def translate_text(text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """


    translate_client = translate.Client()

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(text, target_language="en-US")

    print(u"Text: {}".format(result["input"]))
    print(u"Translation: {}".format(result["translatedText"]))
    print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))


if __name__ == "__main__":
    # translate_text("я люблю тебя")


    #export GOOGLE_APPLICATION_CREDENTIALS="/Users/stanislavivanov/Downloads/my-project-98575-371210-114ac428d015.json"


    prompt = """Write love letter to my real girlfriend named Daria using references to anime Naruto"""
    resp = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=300, temperature=0.9, top_p=1, frequency_penalty=0.0, presence_penalty=0.6)
    print(resp)
    text = resp.choices[0].text
    print(text)
    
