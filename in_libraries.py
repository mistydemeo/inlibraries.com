from flask import Flask
from flask import render_template
from flask import render_template_string
from flask import request
from datetime import date
from random import randint
import json

app = Flask(__name__)

# Load synonyms
synonyms_json = open("synonyms.json").read()
synonyms = json.loads(synonyms_json)

# Load session madlibs
session_madlibs_json = open("session_madlibs.json").read()
session_madlibs = json.loads(session_madlibs_json)

# part = part of speech (noun, verb, etc)
# word = specific word to get a synonym for
# refer to synonyms.json
def get_synonym(part, word):
    synonyms_for_word = synonyms[part][word]
    random_number = randint(0, len(synonyms_for_word)-1)
    return synonyms_for_word[random_number]

# Set up Jinja tag for synonym usage in templates
app.jinja_env.globals.update(synonym=get_synonym)

# Front page route
@app.route('/')
def front_page(subdomain=None):
    subdomain_split = request.host.split(".")[0].split("_")
    subdomain = " ".join(subdomain_split)
    subdomain_title = subdomain.title()
    year = date.today().year

    def get_random_session_madlib():
        random_number = randint(0, len(session_madlibs)-1)
        template_string = session_madlibs[random_number]
        return render_template_string(template_string, subdomain=subdomain, subdomain_title=subdomain_title, year=year)

    # Set up Jinja tag for random session madlib in templates
    app.jinja_env.globals.update(random_session=get_random_session_madlib)
    
    return render_template('front_page.html', subdomain=subdomain, subdomain_title=subdomain_title, year=year)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
