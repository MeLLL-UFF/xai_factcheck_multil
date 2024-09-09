# X-fact constants
XFACT_LABELS = {'false': 0,
 'partly true/misleading':1,
 'true': 2,
 'mostly true': 3,
 'mostly false': 4,
 'complicated/hard to categorise': 5, 
 'other': 6
}


XFACT_LABEL2IDX = {label:idx for idx, label in enumerate(XFACT_LABELS)}
XFACT_IDX2LABEL = {idx:label for idx, label in enumerate(XFACT_LABELS)}

LANG_CODE2COUNTRY = {'tr': 'Turkey',
 'ka': 'Georgia',
 'pt': 'Brazil',
 'id': 'Indonesia',
 'sr': 'Serbia',
 'it': 'Italy',
 'de': 'Germany',
 'ro': 'Romania',
 'ta': 'Sri Lanka',
 'pl': 'Poland',
 'hi': 'India',
 'ar': 'Middle East',
 'es': 'Spain',
 'ru': 'Russia',
 'mr': 'Indian state of Maharashtra',
 'sq': 'Albania',
 'gu': 'Indian state of Gujarat',
 'fr': 'France',
 'no': 'Norway',
 'si': 'Sri Lanka',
 'nl': 'Netherlands',
 'az': 'Azerbaijan',
 'bn': 'Bangladesh',
 'fa': 'Persia',
 'pa': 'Indian state of Punjab'}

MONOLINGUAL_LANGUAGES=['ar','fr','fa','ru','id','pt'] 