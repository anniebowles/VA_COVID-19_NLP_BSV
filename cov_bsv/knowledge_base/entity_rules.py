entity_rules = [
    {'label': "ORG", "pattern": "VA"},
    {'label': "ORG", "pattern": [{"LOWER":"non"}, {"ORTH":"-", "OP": "?"}, {"LOWER":"va"}, {"LOWER":"facility"}]},
    {'label': "ORG", "pattern": "CVS"},
    {'label': "PRODUCT", "pattern": [{"LOWER":"cprs"}]},
    {'label': "PRODUCT", "pattern": [{"LOWER":"epic", "OP": "?"}, {"LOWER":"ehr"}]},
    {"label": "DATE", "pattern": [{"LOWER": {"REGEX": "\d{1,4}(\\|-|/)\d{1,2}(\\|-|/)\d{1,4}$"}}]},
    {"label": "DATE", "pattern":[{"LOWER": "on"},{"LOWER": {"REGEX": "\d{1,2}(\\|-|/)\d{1,2}$"}}]},
    {"label": "DATE","pattern":[{"LOWER": {"IN": ["january","february","march","april","may","june","july","august","september","october","november","december","jan","feb","mar","apr","may","jun","jul","aug","sept","oct","nov","dec"]}},{"IS_DIGIT": True, "LENGTH": 2},{"ORTH": ",", "OP": "?"},{"IS_DIGIT": True, "LENGTH": 4, "OP": "?"}]}, #when there is a space between the day and year
    {"label": "DATE","pattern":[{"LOWER": {"IN": ["january","february","march","april","may","june","july","august","september","october","november","december","jan","feb","mar","apr","may","jun","jul","aug","sept","oct","nov","dec"]}},{"LOWER": {"REGEX": "\d{1,2},\d{2,4}"}}]}, #when there is no space after the comma
    {"label": "DATE", "pattern":[{"IS_DIGIT": True, "LENGTH": 2},{"ORTH": {"IN": ["-","/"]}},{"IS_DIGIT": True, "LENGTH": 2},{"ORTH": {"IN": ["-","/"]}},{"IS_DIGIT": True, "LENGTH": 4}]},
    {"label": "DATE", "pattern":[{"IS_DIGIT": True, "LENGTH": 2},{"ORTH": {"IN": ["-","/"]}},{"IS_DIGIT": True, "LENGTH": 2},{"ORTH": {"IN": ["-","/"]}},{"IS_DIGIT": True, "LENGTH": 2}]},
    {"label": "DATE", "pattern":[{"IS_DIGIT": True, "LENGTH": 4},{"ORTH": {"IN": ["-","/"]}},{"IS_DIGIT": True, "LENGTH": 2},{"ORTH": {"IN": ["-","/"]}},{"IS_DIGIT": True, "LENGTH": 2}]},
    {"label": "DATETIME", "pattern":[{"LOWER": {"REGEX": "\d{1,2}(\\|-|/)\d{1,2}@\d{2,4}$"}}]}
]