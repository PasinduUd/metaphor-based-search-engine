import pandas as pd

# Read the CSV file
df = pd.read_csv("Data\sinhala_songs_corpus.csv")
df = df.drop(["ID"], axis=1)

# Convert the DataFrame to a JSON file
df.to_json("Data\sinhala_songs_corpus.json", orient="records")