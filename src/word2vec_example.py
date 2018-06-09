from gensim.models.wrappers import FastText

model = FastText.load_fasttext_format('../data/raw/BIN/wiki.simple')

print(model.most_similar('brain'))

print(model.similarity('brain', 'synapse'))

print(model.wv.most_similar(positive=['Trump'], negative=['president']))
