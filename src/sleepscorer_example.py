from sleepscorer import Classifier
import mne
epochs_clean = mne.read_epochs('../data/derived/cleaned_epo.fif')
epochs_clean = epochs_clean.filter(0.15, None)
epochs_clean = epochs_clean.resample(100, npad='auto')

data = epochs_clean.get_data() # load your python array, preprocessed
# assert(data.ndim==3 and data.shape[1:]==(3000,3))

clf = Classifier()
# clf.download_weights()  # skip this if you already downloaded them.
# https://www.dropbox.com/s/otm6t0u2tmbj7sd/cnn.hdf5?dl=1
# https://www.dropbox.com/s/t6n9x9pvt5tlvj8/rnn.hdf5?dl=1
clf.load_cnn_model('./weights/cnn.hdf5')
clf.load_rnn_model('./weights/rnn.hdf5')
preds = clf.predict(data, classes=True)