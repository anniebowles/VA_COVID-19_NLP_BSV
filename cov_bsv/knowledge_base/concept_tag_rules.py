from medspacy.ner import TargetRule

concept_tag_rules = {
    "test": [
        TargetRule(literal="nasal swab", category="TEST",
              pattern=[{'LOWER': "nasal"}
                       ,{"LOWER": "swab"}]),
        TargetRule(literal="test for", category="TEST",
              pattern=[{"LOWER": {"REGEX": "^test"}}, {"LOWER": "for", "OP": "?"}]),
        TargetRule(literal="retest for", category="TEST",
              pattern=[{"LOWER": {"REGEX": "^retest"}}, {"LOWER": "for", "OP": "?"}]),
        TargetRule(literal="check for", category="TEST",
              pattern=[{"LOWER": {"REGEX": "^check"}, "POS": "VERB"}, {"LOWER": "for"}]),
        TargetRule(literal="work up", category="TEST",
              pattern=[{"LOWER": "work"}, {"LOWER": "-", "OP": "?"}, {"LOWER": "up"}]),
        TargetRule(literal="workup", category="TEST"),
        TargetRule(literal="results", category="TEST"),
        TargetRule(literal="evaluation", category="TEST"),
        TargetRule(literal="evaluated for", category="TEST",
              pattern=[{"LOWER": {"REGEX": "^eval"}}, {"LOWER": "for"}]),
        TargetRule(literal="swab", category="TEST"),
        TargetRule(literal="PCR", category="TEST",
                pattern=[
                    {"LOWER": "pcr", "OP": "?"},
                    {"IS_SPACE": True, "OP": "*"},
                    {"LOWER": "lab"},
                    {"IS_SPACE": True, "OP": "*"},
                    {"LOWER": "test"}]),
        TargetRule(literal="Non-PCR", category="TEST",
                pattern=[{"LOWER":"non"},
                    {"ORTH":"-", "OP": "?"},
                    {"LOWER": "pcr", "OP": "?"},
                    {"IS_SPACE": True, "OP": "*"},
                    {"LOWER": "lab"},
                    {"IS_SPACE": True, "OP": "*"},
                    {"LOWER": "test"}]),
    TargetRule(literal="specimen sent", category="TEST"),
    ],
    "external_location": [
        TargetRule(
            literal="non-VA facility",
            category="external_location",
            pattern=[{"LOWER":"non"}
            ,{"ORTH":"-", "OP": "?"}
            ,{"LOWER":"va"}
            ,{"LOWER": {"IN":["facility","hospital","site","clinic",
                                          "medical center", "nursing home",'lab',
                                         "location","provider"]}}]),
        TargetRule(literal="outside facility", category="external_location",
              pattern=[{'LOWER': {"IN": ['outside', "community"]}}
                       ,{"LOWER": {"IN": ["facility","hospital","site","clinic",
                                          "medical center", "nursing home",'lab',
                                         "location","provider"]}}]),
    #non-VA
    TargetRule(literal="non VA facility", category="external_location",
              pattern=[{'LOWER': 'non'}
                       ,{"ORTH": "-", "OP": "?"}
                       ,{"LOWER": "va"}]),
    #test done at a location other than this VA.
    TargetRule(literal="a location other than this VA", category="external_location",
              pattern=[{'LOWER': "a"}, {"IS_SPACE":True, "OP": "*"}, {'LOWER': "location"}, {"IS_SPACE":True, "OP": "*"}, {'LOWER': "other"}, {"IS_SPACE":True, "OP": "*"}, {'LOWER': "than"}, {"IS_SPACE":True, "OP": "*"}, {'LOWER': "this"}, {"IS_SPACE":True, "OP": "*"}, {'LOWER': "va"}]),
    #COVID-19 Outside Test Results POSITIVE
    TargetRule(literal="Outside Test Results", category="external_location",
              pattern=[{'LOWER': 'outside'}
                       ,{"LOWER": "test"}
                      ,{"LOWER": "results"}]),
    # PRIV SECTR
    TargetRule(literal="private sector", category="external_location",
              pattern=[{'LOWER': {"IN": ['private','priv']}}
                       ,{'LOWER': {"IN": ['sector','sectr']}}]),
    #community urgent care
    TargetRule(literal="community urgent care", category="external_location",
              pattern=[{'LOWER': {"IN": ['community','an','local']}}
                       ,{"LOWER": "urgent"}
                      ,{"LOWER": "care"}])
    ],
    "coronavirus": [
        TargetRule(
            literal="coronavirus",
            category="COVID-19",
            pattern=[{"LOWER": {"REGEX": "coronavirus|hcov|ncov$"}}],
        ),
        TargetRule(
            literal="covid",
            category="COVID-19",
            pattern=[{"LOWER": {"REGEX": "^covid"}}],
        ),
        TargetRule(literal="Novel Coronavirus (COVID-19)", category="COVID-19"),
        TargetRule(literal="novel coronavirus", category="COVID-19"),
        TargetRule(
            literal="[{'LOWER': {'REGEX': '^covid-19'}}]",
            category="COVID-19",
            pattern=[{"LOWER": {"REGEX": "^covid-19"}}],
        ),
        TargetRule(
            literal="[{'LOWER': 'sars'}, {'LOWER': '-', 'OP': '?'}, {'LOWER': 'cov-2'}]",
            category="COVID-19",
            pattern=[{"LOWER": "sars"}, {"LOWER": "-", "OP": "?"}, {"LOWER": "cov-2"}],
        ),
        
        TargetRule(literal="cov2", category="COVID-19"),
        TargetRule(literal="ncov-19", category="COVID-19"),
        TargetRule(literal="novel coronavirus 2019", category="COVID-19"),
        TargetRule(literal="novel corona", category="COVID-19"),
        TargetRule(literal="covid-10", category="COVID-19"),
        TargetRule(literal="corona 2019", category="COVID-19"),
        TargetRule(literal="coronavirus 19", category="COVID-19"),
        TargetRule(literal="covd-19", category="COVID-19"),
        TargetRule(literal="COVID-19", category="COVID-19"),
        TargetRule(literal="CoV19", category="COVID-19", pattern=[{"LOWER": "cov19"}]),
        TargetRule(literal="COVID-19 PCR Lab test", category="COVID-19", 
                    pattern=[{"LOWER": "covid-19"},#{"ORTH": "-"},{"ORTH": "19"},
                    {"IS_SPACE": True, "OP": "*"},
                    {"LOWER": "pcr", "OP": "?"},
                    {"IS_SPACE": True, "OP": "*"},
                    {"LOWER": "lab"},
                    {"IS_SPACE": True, "OP": "*"},
                    {"LOWER": "test"}]
        ),
        TargetRule(
            literal="COVID 19",
            category="COVID-19",
            pattern=[
                {"LOWER": "covid"},
                {"IS_SPACE": True, "OP": "*"},
                {"ORTH": "19"}
            ],
        ),
        TargetRule(literal="covd 19", category="COVID-19"),
        TargetRule(literal="covid 19", category="COVID-19", 
            pattern=[{"LOWER": {"REGEX": "covid\s*19"}}]),
        TargetRule(literal="SARS-CoV-2", category="COVID-19"),
        TargetRule(literal="SARS-CoV2", category="COVID-19"),
        TargetRule(literal="SARS-CoVID-2", category="COVID-19"),
        TargetRule(literal="SARS CoV", category="COVID-19"),
        TargetRule(literal="SARS-CoV-19", category="COVID-19"),
        TargetRule(literal="no-cov", category="COVID-19"),
        TargetRule(
            literal="coivid",
            category="COVID-19",
            pattern=[{"LOWER": {"REGEX": "^coivid"}}],
        ),
    ],
    "positive": [
        TargetRule("+", "positive", pattern=[{"LOWER": {"REGEX": "\+$"}}]),
        TargetRule("(+)", "positive"),
        TargetRule("+ve", "positive"),
        TargetRule("+ ve", "positive"),
        TargetRule("positive", "positive", pattern=[{"LOWER": {"IN": ['positive','pos','postive']}}]),
        TargetRule("active", "positive"),
        TargetRule("confirmed", "positive"),
        TargetRule(
            "results positive",
            "positive",
            pattern=[
                {"LOWER": "results"},
                {"LEMMA": "be", "OP": "?"},
                {"LOWER": {"IN": ["pos", "positive"]}},
            ],
        ),
    ],
    "associated_diagnosis": [
        TargetRule(
            literal="pneumonia",
            category="associated_diagnosis",
            pattern=[{"LOWER": {"IN": ["pneumonia", "pneum", "pna"]}}],
        ),
        TargetRule(literal="ards", category="associated_diagnosis"),
        TargetRule(
            literal="ards",
            category="associated_diagnosis",
            pattern=[
                {"LOWER": "ards"},
                {"LOWER": "(", "OP": "?"},
                {"LOWER": {"REGEX": "[12]/2"}},
                {"LOWER": ")", "OP": "?"},
            ],
        ),
        # may be too imprecise, but I have seen Coronavirus infection 
         TargetRule(literal="infection", category="associated_diagnosis"),
        # TargetRule(literal="illness", category="associated_diagnosis"),
        TargetRule(
            literal="respiratory failure",
            category="associated_diagnosis",
            pattern=[{"LOWER": {"REGEX": "resp"}}, {"LOWER": "failure"},],
        ),
        TargetRule(
            "respiratory failure 2/2",
            "associated_diagnosis",
            pattern=[
                {"LOWER": {"IN": ["hypoxemic", "acute", "severe"]}, "OP": "+"},
                {"LOWER": {"REGEX": "resp"}},
                {"LOWER": "failure"},
                {"LOWER": "(", "OP": "?"},
                {"LOWER": {"REGEX": "[12]/2"}},
                {"LOWER": ")", "OP": "?"},
            ],
        ),
        TargetRule("hypoxia", "associated_diagnosis"),
        TargetRule("septic shock", "associated_diagnosis"),
        # TargetRule("sepsis", "associated_diagnosis"),
    ],
    "diagnosis": [
        TargetRule(
            "diagnosis",
            "diagnosis",
            pattern=[
                #{"LOWER": "a"},
                {"LOWER": {"IN": ["diagnosis", "dx", "dx."]}},
                {"LOWER": "of", "OP": "?"},
            ],
        ),
        TargetRule(
            "diagnosed with",
            "diagnosis",
            pattern=[
                {"LOWER": {"IN": ["diagnosed", "dx", "dx.", "dx'd"]}},
                {"LOWER": "with"},
            ],
        ),
    ],
    "screening": [
        TargetRule("screen", "screening", pattern=[{"LOWER": {"REGEX": "^screen"}}]),
    ],
    "patient": [
        TargetRule(
            "patient",
            category="patient",
            pattern=[{"LOWER": {"IN": ["patient", "pt", "pt."]}}],
        ),
        TargetRule(
            "veteran",
            category="patient",
            pattern=[{"LOWER": {"IN": ["veteran", "vet"]}}],
        ),
    ],
    # These rules are meant to capture mentions of other family members,
    # Sometimes this will be referring to a family member who tested positive
    "family": [
        TargetRule(
            "family member",
            category="family",
            pattern=[
                {
                    "POS": {"IN": ["NOUN", "PROPN", "PRON"]},
                    "LOWER": {
                        "IN": [
                            "wife",
                            "husband",
                            "spouse",
                            "family",
                            "member",
                            "girlfriend",
                            "boyfriend",
                            "mother",
                            "father",
                            "nephew",
                            "niece",
                            "grandparent",
                            "grandparents",
                            "granddaughter",
                            "grandchild",
                            "grandson",
                            "cousin",
                            "grandmother",
                            "grandfather",
                            "parent",
                            "son",
                            "daughter",
                            "mom",
                            "dad",
                            "brother",
                            "sister",
                            "aunt",
                            "uncle",
                            "child",
                            "children",
                            "sibling",
                            "siblings",
                            "relative",
                            "relatives",
                            "caregiver",
                        ]
                    },
                }
            ],
        )
    ],
    "timex": [
        TargetRule(
            "<NUM> <TIME> <AGO>",
            category="timex",
            pattern=[
                {"LIKE_NUM": True},
                {"LOWER": {"IN": ["days", "day", "weeks", "week", "month", "months"]}},
                {"LOWER": {"IN": ["ago", "prior"]}},
            ],
        ),
    ],
    # These rules are meant capture mentions of COVID-19 + individuals
    # other than the patient and family members.
    "other_experiencer": [
        TargetRule(
            "other experiencer",
            category="other_experiencer",
            pattern=[
                {
                    "POS": {"IN": ["NOUN", "PROPN", "PRON", "ADJ"]},
                    "LOWER": {
                        "IN": [
                            "someone",
                            "somebody",
                            "person",
                            "anyone",
                            "anybody",
                            "people",
                            "individual",
                            "individuals",
                            "teacher",
                            "anybody",
                            "employees",
                            "employer",
                            "customer",
                            "client",
                            "residents",
                            "resident(s",
                            "pts",
                            "patients",
                            "coworker",
                            "coworkers",
                            "workers",
                            "colleague",
                            "captain",
                            "captains",
                            "pilot",
                            "pilots",
                            "wife",
                            "husband",
                            "spouse",
                            "family",
                            "member",
                            "girlfriend",
                            "boyfriend",
                            "persons",
                            "person(s",
                            "church",
                            "convention",
                            "guest",
                            "party",
                            "attendee",
                            "conference",
                            "roommate",
                            "friend",
                            "friends",
                            "coach",
                            "player",
                            "neighbor",
                            "manager",
                            "boss",
                            "cashier",
                            "landlord",
                            "worked",
                            "works",
                            "nobody",
                            # "mate",
                            "mates",
                            "housemate",
                            "housemates",
                            "hotel",
                            "soldier",
                            "airport",
                            "tsa",
                            "lady",
                            "ladies",
                            "lobby",
                            "staffer",
                            "staffers",  # "staff",
                            "sailor",
                            "sailors",
                            "meeting",
                        ]
                    },
                }
            ],
        ),
        TargetRule(
            "the women",
            "other_experiencer",
            pattern=[{"LOWER": {"IN": ["the", "a"]}}, {"LEMMA": "woman"}],
        ),
        TargetRule(
            "the men",
            "other_experiencer",
            pattern=[{"LOWER": {"IN": ["the", "a"]}}, {"LEMMA": "man"}],
        ),
        TargetRule("in contact with", "other_experiencer"),
        TargetRule("any one", "other_experiencer"),
        TargetRule("co-worker", "other_experiencer"),
        TargetRule("at work", "other_experiencer"),
        TargetRule(
            "another patient",
            "other_experiencer",
            pattern=[{"LOWER": "another"}, {"LOWER": {"IN": ["pt", "patient", "pt."]}}],
        ),
        TargetRule(
            "a patient",
            "other_experiencer",
            pattern=[{"LOWER": "a"}, {"LOWER": {"IN": ["pt", "patient", "pt."]}}],
        ),
    ],
    
}
