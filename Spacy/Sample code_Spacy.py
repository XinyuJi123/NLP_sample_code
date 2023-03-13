#!/usr/bin/env python
# coding: utf-8

# In[12]:


#env python3
# -*- coding: utf-8 -*-
#current numpy version is 1.21

"""
This sample module extracts researcher names from news article content by Spacy package.
For the purpose of demonstration, I extracted news from "Science Daily" website,(https://www.sciencedaily.com/)

Steps: 1. Get news titles for future use, such as pair up with interviewed researchers.
       2. Data cleaning and get researcher names from news content.
       3. Label researcher genders and for future use, by Javascript and HTML magic cells.

Outputs: All three output json files are saved in child folder "News", including:
         1. json file containing news titles.
         2. json file containing researcher names.
         3. json file containing researcher genders. 

@author: Xinyu Ji GitHub: https://github.com/XinyuJi123
Common disclaimers apply. Subject to change at all time.

Last review: 13/03/2023
"""

import spacy
import os
from datetime import datetime
import re
import json
import glob
from nltk.corpus import stopwords
from spacy.tokens import Span
import en_core_web_sm
#from spacy.lang.en.stop_words import STOP_WORDS

class NLP:
    def __init__(self,write=True):
        self.w=write
        
    def get_article_titles(self):
        write=self.w
        
        file_list = os.listdir("News/") 
        fnames = []
        for fname in file_list:
            fname = fname.split('_')[0]
            fnames.append(fname)
        if write == True:
            with open ('article_titles_Spacy.json', 'w') as output_title:
                output_title.write(json.dumps(fnames))
    
    def get_researcher_names(self):
        write=self.w
        
        person_articles = []
        
        #initiating Spacy nlp pipeline.
        nlp = en_core_web_sm.load()
        stopwords = nlp.Defaults.stop_words
        
        t000=datetime.now()
        for article in glob.glob('News/*.txt'):
            article = open(article, 'r',encoding='utf-8')
            # read all text
            text = article.read()
            # Remove punctuation
            text = re.sub('[,\.!?]', '', text)
            
            #Removing stopwords is not need for the purpose of researcher name extraction. 
            #These are codes for future use.
            #tokens_without_stopwords=[]
            #for token in text.split():
                #if token.lower() not in stopwords:
                    #tokens_without_stopwords.append(token)
            
            #tokens_without_stopwords = str(tokens_without_stopwords)
            
            
            text = nlp(text)
            #Researcher name extraction
            person = [ent.text for ent in text.ents if ent.label_=='PERSON']
            person_articles.append(person)
            
        if write == True:
            with open ('researcher_names_articles_Spacy.json', 'w') as output_name:
                output_name.write(json.dumps(person_articles))
                
                
        t001=datetime.now()
        dt00=t001-t000
        print('Name Extraction is completed after '+str(dt00.total_seconds())+' seconds')


# In[13]:


Spacy=NLP(write=True)
Spacy.get_article_titles()
Spacy.get_researcher_names()


# In[15]:


#The following codes design an interface to label the mentioned researchers from news articles with their genders. 
# Other labels such as race, nationality, and other background factors can also be achieved in a similar way.
#(WIP v1.0 by Javascript and HTML magic cells)


#Initialting input json files preparation.
article_titles = []

with open('article_titles_Spacy.json') as output_title:
    for title in output_title:
        article_titles.append(json.loads(title))

researcher_names = []
        
with open('researcher_names_articles_Spacy.json') as output_name:
    for name in output_name:
        researcher_names.append(json.loads(name))
                
genders = []
if os.path.exists('researcher_gender_articles_Spacy.json'):
    with open('researcher_gender_articles_Spacy.json') as output_gender:
        genders = json.load(output_gender)

researcher_dict = {}
for i in range(len(researcher_names[0])):
    researcher_dict[article_titles[0][i]] = researcher_names[0][i]

#Make sure that we can start labelling from exactly where we left last time                
def get_next_researcher():
    return list(researcher_dict.values())[len(genders)]


# In[16]:


get_ipython().run_cell_magic('javascript', '', '        \nfunction set_gender(gender){\n    var kernel = IPython.notebook.kernel;\n    kernel.execute("genders.append(" + gender + ")");\n    load_next_researcher();\n}\n\nfunction handle_output(out){\n    var res = out.content.data["text/plain"];\n    $("div#researcher").html(res);\n}\n        \nfunction load_next_researcher(){\n    var code_input = "get_next_researcher()";\n    var kernel = IPython.notebook.kernel;\n    var callbacks = { \'iopub\' : {\'output\' : handle_output}};\n    kernel.execute(code_input, callbacks, {silent:false});\n}')


# In[17]:


get_ipython().run_cell_magic('html', '', '<div name="researcherbox">\n    Instructions: Click in textbox. Enter a 1 if the researcher is female, enter 0 otherwise. <br>\nResearcher Name: <div id="researcher" value="text"></div><br>\n<input type=researcher_names id="capture"></input><br>\n</div>\n        \n<script>\n\nfunction set_gender(gender){\n    var kernel = IPython.notebook.kernel;\n    kernel.execute("genders.append(" + gender + ")");\n    load_next_researcher();\n}\n\nfunction handle_output(out){\n    var res = out.content.data["text/plain"];\n    $("div#researcher").html(res);\n}\n        \nfunction load_next_researcher(){\n    var code_input = "get_next_researcher()";\n    var kernel = IPython.notebook.kernel;\n    var callbacks = { \'iopub\' : {\'output\' : handle_output}};\n    kernel.execute(code_input, callbacks, {silent:false});\n}\n\n$("input#capture").keypress(function(e) {\nif(e.which == 48) {\n    set_gender(0);\n    $("input#capture").val("");\n}else if (e.which == 49){\n    set_gender(1);\n    $("input#capture").val("");\n  }\n});\n        \nload_next_researcher();\n</script>')


# In[18]:


with open('researcher_genders_Spacy.json', 'w') as output_gender:
    json.dump(genders,output_gender)

