#!/usr/bin/env python
# coding: utf-8

# In[21]:


#check that the notebook is pointing to your anaconda version, not the master Anaconda folder
#import sys
#sys.path


# ## A note on adjusting the rules
# In order to use your new rules, you have to restart the kernel and re-import the libraries every time you add rules to the knowledge_base files.

# In[1]:


import medspacy
import spacy
import cov_bsv
#from cov_bsv import visualize_doc
from medspacy.visualization import visualize_ent
from medspacy.ner import TargetMatcher, TargetRule
from spacy import displacy

import warnings
warnings.filterwarnings("ignore")


# In[3]:


nlp = cov_bsv.load(disable=['document_classifier', "postprocessor"])
#disbled = nlp.disable_pipes("ner")
nlp.pipeline


# ## Exploring Target Matcher and Rules
# 
# ### From the util.py file...
# - concept_tagger: Assigns a semantic tag in a custom attribute "token._.concept_tag"
# to each Token in a Doc, which helps with concept extraction and normalization.
# Concept tag rules are defined in cov_bsv.knowledge_base.concept_tag_rules.
# - target_matcher: Extracts spans to doc.ents using extended rule-based matching.
# Target rules are defined in cov_bsv.knowledge_base.target_rules.

# ## Dates
# Using the ner model, which comes after the 'concept_tagger', 'target_matcher', and an "entity ruler" with manual date patterns.

# In[12]:


print(spacy.explain("DATE"))


# ## Using entity ruler

# In[4]:


from spacy.pipeline import EntityRuler


# ### From the spacy docs
# The entity ruler is designed to add to the ner. If the entity ruler is added before the ner component, the entity recognizer will respect the existing entity spans and adjust its predictions around it, significantly improving accuracy. If added after the ner component, the entity ruler will only add spans to the doc.ents if they don't overlap with existing entities predicted by the model. 
# 
# TL;DR
# - Entity ruler first: manual labels take precedence
# - Ner first: model labels take precedence

# In[5]:


ruler = EntityRuler(nlp)
patterns = [
    {'label': "ORG", "pattern": "VA"},
    {'label': "ORG", "pattern": [{"LOWER":"non"}, {"ORTH":"-", "OP": "?"}, {"LOWER":"va"}, {"LOWER":"facility"}]},
    {'label': "ORG", "pattern": "CVS"},
    {'label': "PRODUCT", "pattern": [{"LOWER":"cprs"}]},
    {'label': "PRODUCT", "pattern": [{"LOWER":"epic", "OP": "?"}, {"LOWER":"ehr"}]},
    {"label": "DATE", "pattern": [{"LOWER": {"REGEX": "\d{1,4}(\\|-|/)\d{1,2}(\\|-|/)\d{1,4}$"}}]},
    {"label": "DATE", "pattern":[{"LOWER": "on"},{"LOWER": {"REGEX": "\d{1,2}(\\|-|/)\d{1,2}$"}}]},
    {"label": "DATE","pattern":[{"LOWER": {"IN": ["january","february","march","april","may","june","july","august","september"
                                         ,"october","november","december","jan","feb","mar","apr","may","jun","jul"
                                         ,"aug","sept","oct","nov","dec"]}}
                       ,{"IS_DIGIT": True, "LENGTH": 2}
                       ,{"ORTH": ",", "OP": "?"}
                       ,{"IS_DIGIT": True, "LENGTH": 4, "OP": "?"}]}, #when there is a space between the day and year
    {"label": "DATE","pattern":[{"LOWER": {"IN": ["january","february","march","april","may","june","july","august","september"
                                         ,"october","november","december","jan","feb","mar","apr","may","jun","jul"
                                         ,"aug","sept","oct","nov","dec"]}}
                       ,{"LOWER": {"REGEX": "\d{1,2},\d{2,4}"}}]}, #when there is no space after the comma

    {"label": "DATE", "pattern":[{"IS_DIGIT": True, "LENGTH": 2}
                      ,{"ORTH": {"IN": ["-","/"]}}
                      ,{"IS_DIGIT": True, "LENGTH": 2}
                      ,{"ORTH": {"IN": ["-","/"]}}
                      ,{"IS_DIGIT": True, "LENGTH": 4}]},
    {"label": "DATE", "pattern":[{"IS_DIGIT": True, "LENGTH": 2}
                      ,{"ORTH": {"IN": ["-","/"]}}
                      ,{"IS_DIGIT": True, "LENGTH": 2}
                      ,{"ORTH": {"IN": ["-","/"]}}
                      ,{"IS_DIGIT": True, "LENGTH": 2}]},
    {"label": "DATE", "pattern":[{"IS_DIGIT": True, "LENGTH": 4}
                      ,{"ORTH": {"IN": ["-","/"]}}
                      ,{"IS_DIGIT": True, "LENGTH": 2}
                      ,{"ORTH": {"IN": ["-","/"]}}
                      ,{"IS_DIGIT": True, "LENGTH": 2}]},
    {"label":"DATETIME", "pattern":[{"LOWER": {"REGEX": "\d{1,2}(\\|-|/)\d{1,2}@\d{2,4}$"}}]}
]
ruler.add_patterns(patterns)
nlp.add_pipe(ruler, before="ner")


# In[6]:


nlp.pipeline


# In[7]:


dates = """435-908-7890
5/5/2020
March 23, 2020
Apr 26,2020
Jul 22 
3/23/20
10-18-20
Covid negative 4/18@1357
diagnosed with covid on 4/14 at non VA facility
Covid negative on 4/18 at non-va hospital"""


# In[8]:


doc = nlp(dates)
cov_bsv.visualize_doc(doc)


# In[9]:


dates2 = """
    Positive COVID-19 Lab test done at a location other than this VA. Date: March 3, 2021 
    Covid test from last week
    tested covid (+) this morning
    Negative COVID-19 Non-PCR Antigen Lab test done at a location other than this VA. Date: March 4, 2021 
    he tested positive for covid at a community location 1 week ago
    he reports had COVID on  2/8/2021, tested positive at an urgent care.
    Testing Facility: LabCorp Test Date: Apr 14,2020 Result is by: Patient self-report COVID-19 lab test was positive
"""


# In[10]:


doc = nlp(dates2)
cov_bsv.visualize_doc(doc)


# In[11]:


for ent in doc.ents:
    print(ent, ent.label_, sep = " | ")
    print()


# ## Old - using target rules

# In[2]:


#nlp2 = cov_bsv.load(enable=["tagger", "parser"], load_rules=False) 

nlp2 = cov_bsv.load(disable=['concept_tagger','target_matcher','sectionizer','ner','document_classifier'], load_rules=False)


# In[10]:


target_matcher = TargetMatcher(nlp2)
#nlp2.add_pipe(target_matcher)
type(target_matcher)


# In[4]:


target_rules = [
   TargetRule(literal="month day, year", category="DATE",
              pattern=[{"LOWER": {"IN": ["january","february","march","april","may","june","july","august","september"
                                         ,"october","november","december","jan","feb","mar","apr","may","jun","jul"
                                         ,"aug","sept","oct","nov","dec"]}}
                       ,{"IS_DIGIT": True, "LENGTH": 2}
                       ,{"ORTH": ",", "OP": "?"}
                       ,{"IS_DIGIT": True, "LENGTH": 4, "OP": "?"}]),
    TargetRule(literal="day month year", category="DATE",
              pattern=[{"IS_DIGIT": True}
                      ,{"LOWER": {"IN": ["january","february","march","april","may","june","july","august","september"
                                         ,"october","november","december","jan","feb","mar","apr","may","jun","jul"
                                         ,"aug","sept","oct","nov","dec"]}}
                      ,{"IS_DIGIT": True}]),
    TargetRule(literal="dd/mm/yyyy or yyyy/mm/dd", category="DATE",
              pattern=[{"LOWER": {"REGEX": "\d{1,4}(\\|-|/)\d{1,2}(\\|-|/)\d{1,4}$"}}]),
    TargetRule(literal="dd-mm-yyyy", category="DATE",
              pattern=[{"IS_DIGIT": True, "LENGTH": 2}
                      ,{"ORTH": "-", "OP": "?"}
                      ,{"IS_DIGIT": True, "LENGTH": 2}
                      ,{"ORTH": "-", "OP": "?"}
                      ,{"IS_DIGIT": True, "LENGTH": 4}]),
    TargetRule(literal="dd-mm-yy", category="DATE",
              pattern=[{"IS_DIGIT": True, "LENGTH": 2}
                      ,{"ORTH": "-", "OP": "?"}
                      ,{"IS_DIGIT": True, "LENGTH": 2}
                      ,{"ORTH": "-", "OP": "?"}
                      ,{"IS_DIGIT": True, "LENGTH": 2}]),
    TargetRule(literal="yyyy-dd-mm", category="DATE",
              pattern=[{"IS_DIGIT": True, "LENGTH": 4}
                      ,{"ORTH": "-", "OP": "?"}
                      ,{"IS_DIGIT": True, "LENGTH": 2}
                      ,{"ORTH": "-", "OP": "?"}
                      ,{"IS_DIGIT": True, "LENGTH": 2}]),
    TargetRule(literal="dd/mm@tttt", category="DATE",
              pattern=[{"LOWER": {"REGEX": "\d{1,2}(\\|-|/)\d{1,2}@\d{2,4}$"}}]),
    TargetRule(literal="covid",
            category="COVID-19",
            pattern=[{"LOWER": {"REGEX": "^covid"}}])
]

target_matcher.add(target_rules)


# In[4]:


dates = """435-908-7890
5/5/2020
March 23, 2020
Apr 26,2020
Jul 22 
3/23/20
11\15\21
10-18-20
4/14: some event
Covid negative 4/18@1357"""


# In[5]:


#text = """Patient tested negative for novel coronavirus on 02 Apr 20, and positive for covid-19 on May 5, 2020."""
doc = nlp(dates)
cov_bsv.visualize_doc(doc)


# In[7]:


for ent in doc.ents:
    print(ent.text, ent.label_, sep=" -> ")


# ### Example of the difference between the default spaCy and the medspaCy tokenizers

# In[3]:


from medspacy.custom_tokenizer import create_medspacy_tokenizer

nlp = spacy.blank("en")

medspacy_tokenizer = create_medspacy_tokenizer(nlp)
default_tokenizer = nlp.tokenizer

example = r'Jul 22,2020' #r'10-18-20 435-908-7890' #r'December(23rd)'  #r'Pt c/o n;v;d h/o chf+cp'

print("spacy tokenizer:")
print(list(default_tokenizer(example)))
print('\n')
print("medspacy tokenizer:")
print(list(medspacy_tokenizer(example)))
#for ent in doc.ents:
    #print(ent.text, ent.label_, sep=" -> ")


# In[ ]:




