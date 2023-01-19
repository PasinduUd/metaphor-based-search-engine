from googletrans import Translator
import io
import json
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk import word_tokenize
import nltk

# nltk.download('stopwords')
# nltk.download('punkt')

def translate_to_english(query:str):
    translator = Translator()
    english_term = translator.translate(query, dest='en')
    return english_term.text

def remove_stop_words(query:str):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(query)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    # remove punctuation and possessive terms
    filtered_sentence = [w for w in filtered_sentence if not (w == "'s")]
    filtered_sentence = ' '.join(filtered_sentence).translate(str.maketrans('', '', string.punctuation))
    print("Filtered sentence: ", filtered_sentence)
    return filtered_sentence

def check_similarity(documents):
    tfidfvectorizer = TfidfVectorizer(analyzer="char", token_pattern=u'(?u)\\b\w+\\b')
    tfidf_matrix = tfidfvectorizer.fit_transform(documents)

    cs = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    similarity_list = cs[0][1:]
    return similarity_list

def keyword_classifier(query:str):
    select_type = -1    # -1: No keywords identified, 0: 
    result_word = ''
    field_intent = ''

    keyword_metaphor_meaning = ["Metaphor", "meaning of metaphor", "metaphor meaning", "metaphor about", "metaphor related"]
    keyword_source = ["Source Domain","Source_domain", "metaphor_source_domain"]
    keyword_target = ["Target Domain", "Target_domain",  "metaphor_target_domain"]
    keyword_artist = ["Singer(s)", "Artist", "sing_by", "sung_by"]
    keyword_lyricist = ["Lyricist", "writer", "written_by"]

    keyword_fields = [keyword_metaphor_meaning, keyword_source, keyword_target, keyword_artist, keyword_lyricist]
    query = remove_stop_words(query)
    search_term_list = query.split()

    query_words = search_term_list.copy()
    for i in search_term_list:
        for keyword_list in keyword_fields:
            documents = [i]
            documents.extend(keyword_list)

            max_val = max(check_similarity(documents))
            if max_val > 0.85:
                select_type = 0
                field_intent = keyword_list[0]
                print("field intent: " + field_intent)
                query_words.remove(i)

    result_word = ' '.join(query_words)

    print("select_type: {}, result_word: {}, field_intent: {} ".format(select_type, result_word, field_intent))
    return select_type, result_word, field_intent

def search_text(search_term, es):
    results = es.search(index="sinhala-songs-corpus", body={
        "size": 100,
        "query": {
            "multi_match": {
                "query": search_term,
                "type": "best_fields",
                "fields": [
                    "Title", "Singer(s)", "Lyricist", "Musician", "Album", "Released Year",
                    "Lyrics", "Metaphor", "Source Domain", "Target Domain", "Meaning"
                ]
            }
        }
    })
    return results

def search_text_multi_match(search_term, select_type, field_intent, es):
    query_term = search_term
    if select_type == -1:
        english_term = translate_to_english(search_term)
    else:
        english_term = search_term

    f = io.open('../Data/songs_metadata.json', mode="r", encoding="utf-8")
    meta_data = json.loads(f.read())

    data=[]
    if field_intent == "Metaphor":
        field_intent = "Meaning"
        data = meta_data["meaning"]
    elif field_intent == "Source Domain":
        data = meta_data["source"]
    elif field_intent == "Target Domain":
        data = meta_data["target"]
    elif field_intent == "Singer(s)":
        data = meta_data["artist"]
    elif field_intent == "Lyricist":
        data = meta_data["lyricist"]

    documents_meanings = [english_term]
    documents_meanings.extend(data)

    similarity_list = check_similarity(documents_meanings)

    max_val = max(similarity_list)
    if max_val > 0.90:
        loc = np.where(similarity_list == max_val)
        i = loc[0][0]
        query_term = data[i]  # if name is found, search for that to avoid spelling errors

    print("Searched in index: ", query_term)

    results = es.search(index="sinhala-songs-corpus", body={
        "size": 100,
        "query": {
            "multi_match": {
                "query": query_term,
                "type": "best_fields",
                "fields": [field_intent]
            }
        },
    })
    return results

def search_user_query(query, es):
    traslated_query = translate_to_english(query)
    print("Translated : ", traslated_query)

    select_type, strip_term, field_intent = keyword_classifier(traslated_query)
    resp = None
    if select_type == -1:
        resp = search_text(query, es)
    else:
        if strip_term:
            resp = search_text_multi_match(strip_term, select_type, field_intent, es)
        else:
            resp = search_text_multi_match(search_term, select_type, field_intent, es)

    return resp