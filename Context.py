#!/usr/bin/env python
# coding: utf-8

# In[1]:


import medspacy
import spacy
from medspacy.context import ConTextRule, ConTextComponent
from spacy.tokens import Span

import cov_bsv
from medspacy.visualization import visualize_ent, visualize_dep
#from medspacy.ner import TargetMatcher, TargetRule
from spacy import displacy
#from spacy.pipeline import EntityRuler

import warnings
warnings.filterwarnings("ignore")


# In[2]:


nlp = cov_bsv.load(disable=['document_classifier', "postprocessor"])
disbled = nlp.disable_pipes("ner")
nlp.pipeline


# In[3]:


text = "Patient reports that they had a Positive COVID-19 PCR Lab test done at a location other than this VA. Date: February 18, 2021 Location: Memorial Hospital"
#text = "Patient reports that they had a Positive COVID-19 PCR Lab test done at a diagnosis of something. Date: February 18, 2021 Location: Memorial Hospital"


doc = nlp(text)


# In[4]:


displacy.render(doc, style="ent")


# In[5]:


visualize_dep(doc)


# In[6]:


for target, modifier in doc._.context_graph.edges:
    print(modifier._context_rule)
    print("{0} is modified by {1}".format(target, modifier))


# In[ ]:


for ent in doc.ents:
    if any([ent._.is_uncertain, ent._.is_negated, ent._.is_positive, ent._.is_other_experiencer  ]):
        print(" '{0}' modified by {1} in sentence: '{2}'".format(ent, ent._.concept_tag, ent.sent) )
        print()


# ## Testing new context rules

# In[15]:


# instantiate context and pass in an empty knowledge base
context = ConTextComponent(nlp, rules=None)

rules = [ConTextRule(
            literal="covid test done at external location",
            category="EXTERNAL_TEST",
            direction="BACKWARD",
            pattern=[
                {'LOWER': "done", "OP": "?"},
                {"IS_SPACE": True, "OP": "*"},
                {'LOWER': "at"},
                {"IS_SPACE": True, "OP": "*"},
                #{'LOWER': "a"}, {"IS_SPACE":True, "OP": "*"}, 
                {"_": {"concept_tag": "external_location"}}],
            allowed_types={"COVID-19", "OTHER_CORONAVIRUS"})]

#add the rules to the context component
context.add(rules)


# In[16]:


context.rules


# In[17]:


for ent in doc.ents:
    print(ent)
    print("is positive: ", ent._.is_positive)
    print("is external: ", ent._.is_external)


# In[9]:


visualize_dep(doc)


# In[10]:


for target, modifier in doc._.context_graph.edges:
    print(modifier._context_rule)
    print("{0} is modified by {1}".format(target, modifier))


# ### Example of the difference between the default spaCy and the medspaCy tokenizers

# In[ ]:


print(nlp.tokenizer)


# In[5]:


from medspacy.custom_tokenizer import create_medspacy_tokenizer

nlp = spacy.blank("en")

medspacy_tokenizer = create_medspacy_tokenizer(nlp)
default_tokenizer = nlp.tokenizer

example = r'Non-PCR Lab test' #r'10-18-20' #r'Pt c/o n;v;d h/o chf+cp'

print("spacy tokenizer:")
print(list(default_tokenizer(example)))
print('\n')
print("medspacy tokenizer:")
print(list(medspacy_tokenizer(example)))
#for ent in doc.ents:
    #print(ent.text, ent.label_, sep=" -> ")


# In[ ]:


#text = []
with open("O:\\VINCI_COVIDNLP\\va_external_c19_tests\\examples\\outside_test.txt", 'r') as reader:
    text = reader.read()


#print(text)

