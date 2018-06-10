# https://github.com/skjerns/AutoSleepScorer
from sleepscorer import Classifier
from sleepscorer.tools import plot_hypnogram
import mne
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(42)


# Load cleaned epochs
epochs_clean = mne.read_epochs('../data/derived/cleaned_sleep_scorer_epo.fif')

# Format for Sleep Scorer
data = epochs_clean.get_data() # load your python array, preprocessed
data = data[:,np.array([8, 31, 229]),:3000]
data = np.transpose(data, (0, 2, 1))
assert(data.ndim==3 and data.shape[1:]==(3000,3))


# Run Sleep Scorer
clf = Classifier()
# clf.download_weights()  # skip this if you already downloaded them.
# https://www.dropbox.com/s/otm6t0u2tmbj7sd/cnn.hdf5?dl=1
# https://www.dropbox.com/s/t6n9x9pvt5tlvj8/rnn.hdf5?dl=1
clf.load_cnn_model('./weights/cnn.hdf5')
clf.load_rnn_model('./weights/rnn.hdf5')
preds = clf.predict(data, classes=True)

# Plot the hypnogram
plot_hypnogram(preds)
plt.show()