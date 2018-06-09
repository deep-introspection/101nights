from gensim.models.wrappers import FastText

model = FastText.load_fasttext_format('../data/raw/BIN/wiki.simple')

# Give the embedding of a given word
print(model.wv['brain'])
      
# Test if a word is in the model
print('brain' in model.wv.vocab)

# Give the most similar words
print(model.most_similar('brain'))

# Compute similarity between two words
print(model.similarity('brain', 'synapse'))

# Make arithmetic with words
print(model.wv.most_similar(positive=['king', 'woman'], negative=['man']))
