import json
import requests

from app import application

def translate(text, destLanguage,  sourceLanguage):
    if 'YANDEX_DICTIONARY_KEY' not in application.config or \
           not application.config['YANDEX_DICTIONARY_KEY']:
        return ('Error: the translation service is not configured.')

        
    r = requests.get('https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={}&lang={}-{}&text={}'.format(application.config['YANDEX_DICTIONARY_KEY'],  sourceLanguage, destLanguage, text))
    if r.status_code != 200:
        return ('Error: the translation service failed.')
    
    return json.loads(r.content.decode('utf-8-sig'))

