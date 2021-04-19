#!/usr/bin/env python
# coding: utf-8

# In[21]:


#check that the notebook is pointing to your anaconda version, not the master Anaconda folder
#import sys
#sys.path


# ## A note on adjusting the rules
# You have to restart the kernel and re-import the libraries every time you add rules to the knowledge_base files.

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


# ## Sections

# In[9]:


nlp = cov_bsv.load(enable=["tagger", "parser", "concept_tagger", "target_matcher", "sectionizer"])


# In[10]:


doc = nlp(text)


# In[11]:


visualize_ent(doc)
#visualize_dep(doc)


# In[12]:


for ent in doc.ents:
    print(ent)
    print("Uncertain:", ent._.is_uncertain)
    print("Negated:", ent._.is_negated)
    print("Positive:", ent._.is_positive)
    print("Tested outside VA:", ent._.is_external)
    print("Experienced by someone else:", ent._.is_other_experiencer)
    print()


# ### Example of the difference between the default spaCy and the medspaCy tokenizers

# In[7]:


from medspacy.custom_tokenizer import create_medspacy_tokenizer

nlp = spacy.blank("en")

medspacy_tokenizer = create_medspacy_tokenizer(nlp)
default_tokenizer = nlp.tokenizer

example = r'December(23rd)' #r'Jul 22, 2020' #text[2] #r'10-18-20' #r'Pt c/o n;v;d h/o chf+cp'

print("spacy tokenizer:")
print(list(default_tokenizer(example)))
print('\n')
print("medspacy tokenizer:")
print(list(medspacy_tokenizer(example)))
#for ent in doc.ents:
    #print(ent.text, ent.label_, sep=" -> ")

