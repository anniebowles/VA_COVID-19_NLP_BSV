#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#check that the notebook is pointing to your anaconda version, not the master Anaconda folder
#import sys
#sys.path


# ## A note on adjusting the rules
# In order to use your new rules, you have to restart the kernel and re-import the libraries every time you add rules to the knowledge_base files.

# In[ ]:


import medspacy
import spacy
import cov_bsv
#from cov_bsv import visualize_doc
from medspacy.visualization import visualize_ent, visualize_dep
from medspacy.ner import TargetMatcher, TargetRule
from spacy import displacy
from spacy.pipeline import EntityRuler

import warnings
warnings.filterwarnings("ignore")


# In[ ]:


#nlp = cov_bsv.load(model="en_core_web_sm", disable=['document_classifier','ner'], load_rules=True)
#nlp = cov_bsv.load(enable=['tagger','parser','concept_tagger','target_matcher','sectionizer'])
#nlp = cov_bsv.load(enable=['tagger','parser','concept_tagger','target_matcher','sectionizer'])
nlp = cov_bsv.load()
nlp.pipeline


# In[ ]:


text2 = "Patient reports that they had a Positive COVID-19 Lab test done at a location other than this VA. Date: March 6, 2021    Location: CVS Browns Mills Nj"

doc = nlp(text)
doc2 = nlp(text2)


# ### What does the cov_bsv pipeline do out of the box?

# In[ ]:


displacy.render(doc2, style="ent")


# In[ ]:


cov_bsv.visualize_doc(doc2)


# ## Exploring Target Matcher and Rules
# 
# ### From the util.py file...
# - concept_tagger: Assigns a semantic tag in a custom attribute "token._.concept_tag"
# to each Token in a Doc, which helps with concept extraction and normalization.
# Concept tag rules are defined in cov_bsv.knowledge_base.concept_tag_rules.
# - target_matcher: Extracts spans to doc.ents using extended rule-based matching.
# Target rules are defined in cov_bsv.knowledge_base.target_rules.

# ## Outside Locations

# In[ ]:


#nlp2 = cov_bsv.load(disable=['concept_tagger','target_matcher','sectionizer','ner','document_classifier'], load_rules=False)
#nlp2=cov_bsv.load(model='en_core_web_md',enable=['ner'])
nlp2 = cov_bsv.load(disable=["context",'document_classifier', "postprocessor"])

nlp2.pipeline


# ### From the spacy docs
# The entity ruler is designed to add to the ner. If the entity ruler is added before the ner component, the entity recognizer will respect the existing entity spans and adjust its predictions around it, significantly improving accuracy. If added after the ner component, the entity ruler will only add spans to the doc.ents if they don't overlap with existing entities predicted by the model. 
# 
# TL;DR
# - Entity ruler first: manual labels take precedence
# - Ner first: model labels take precedence

# In[ ]:


ruler = EntityRuler(nlp2)
patterns = [
    {'label': "ORG", "pattern": "VA"},
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
nlp2.add_pipe(ruler, before="ner")


# In[ ]:


nlp2.pipeline


# In[ ]:


doc = nlp2(text)


# In[ ]:


displacy.render(doc, style="ent")


# ### Example of the difference between the default spaCy and the medspaCy tokenizers

# In[ ]:


print(nlp.tokenizer)


# In[ ]:


from medspacy.custom_tokenizer import create_medspacy_tokenizer

nlp = spacy.blank("en")

medspacy_tokenizer = create_medspacy_tokenizer(nlp)
default_tokenizer = nlp.tokenizer

example = r'Last Tuesday 2/23' #r'at non VA facility.   Reports'#r'December(23rd)' #r'10-18-20' #r'Pt c/o n;v;d h/o chf+cp'

print("spacy tokenizer:")
print(list(default_tokenizer(example)))
print('\n')
print("medspacy tokenizer:")
print(list(medspacy_tokenizer(example)))
#for ent in doc.ents:
    #print(ent.text, ent.label_, sep=" -> ")


# In[ ]:




