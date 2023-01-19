import json

from googletrans import Translator

translator = Translator()

def translateJson():
    new_list = []
    with open('Data\sinhala_songs_corpus.json') as f:
        list_songs = json.loads(f.read())
        songs = list_songs
        for song in songs:
            translated = {}
            for k, v in song.items():
                translated[k] = v
                if k in ["Title", "Album", "Metaphor"]:
                    translated[k + "_en"] = translator.translate(v, dest="en").text
            new_list.append(translated)
    with open('Data\sinhala_songs_corpus_final.json', 'w+') as f:
        f.write(json.dumps(new_list))


def translateString(data):
    global translator
    if isinstance(data, dict):
        return {k + "_en": translateString(v) for k, v in data.items()}
    else:
        return translator.translate(data, dest="en").text


def metaData():
    metaData = {"title": [], "artist": [], "album": [], "lyricist": [], "metaphor": [], "meaning": [], "source": [],
                "target": []}
    with open('Data\sinhala_songs_corpus.json') as f:
        list_songs = json.loads(f.read())
        songs = list_songs
        for song in songs:
            metaData["title"].append(song["Title"])
            metaData["artist"].append(song["Singer(s)"])
            metaData["album"].append(song["Album"])
            metaData["lyricist"].append(song["Lyricist"])
            metaData["metaphor"].append(song["Metaphor"])
            metaData["meaning"].append(song["Meaning"])
            metaData["source"].append(song["Source Domain"])
            metaData["target"].append(song["Target Domain"])
        with open('Data\songs_metadata.json', 'w+') as f1:
            f1.write(json.dumps(metaData))


if __name__ == "__main__":
    # translateJson()
    metaData()