import html
import random
from html.parser import HTMLParser
import requests
import json

def  load_questions_from_web():


    parameters = {
        "amount": 10,
        "type": "multiple"
    }
    new_dict = {}
    new_dict2 = {}
    count = 0
    questions = {
                    2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
                    4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3}
                    }
    response = requests.get(url="https://opentdb.com/api.php?amount=50&category=22&difficulty=easy&type=multiple", params=parameters)
    question_data = response.json()["results"]
    for i in question_data:
        count += 1
        new_dict = {count:""}
        new_dict[count] = i
        #print(i)
        del new_dict[count]['category']
        del new_dict[count]['type']
        del new_dict[count]['difficulty']

        new_dict[count]['incorrect_answers'].append(new_dict[count]['correct_answer'])
        new_dict[count]['answers'] = new_dict[count].pop('incorrect_answers')
        new_dict[count]['correct'] = new_dict[count].pop('correct_answer')
        random.shuffle(new_dict[count]['answers'])
        sttr= new_dict[count]['answers']
        new_dict[count]['answers'] = html.unescape(sttr)
        sttr = new_dict[count]['correct']
        new_dict[count]['correct'] = html.unescape(sttr)
        sttr = new_dict[count]['question']
        new_dict[count]['question'] = html.unescape(sttr)

        for i,j in new_dict.items():
            new_dict2.update({i:j})

    #print(new_dict2)
    return new_dict2


load_questions_from_web()