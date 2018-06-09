# https://github.com/skjerns/AutoSleepScorer
from sleepscorer import Classifier
import mne
from autoreject import AutoReject, compute_thresholds
from functools import partial
import numpy as np
np.random.seed(42)

path_to_file = '../data/raw/EEG/Nathalie-78_20171118_123017.mff'
raw = mne.io.read_raw_egi(path_to_file,
                          montage='GSN-HydroCel-256',
                          preload=True)

#raw.crop(tmin=3600, tmax=3600*2)
raw.filter(0.15, 50., fir_design='firwin')
raw.resample(100, npad='auto')
raw.set_eeg_reference('average', projection=True)

events = mne.event.make_fixed_length_events(
	raw, id=9999, start=0, stop=None, duration=30.0,
	first_samp=True)
epochs = mne.epochs.Epochs(raw, events, tmin=0, tmax=30.0,
                           baseline=None, preload=True)


thresh_func = partial(compute_thresholds, random_state=42, n_jobs=1)
thresh_functhresh_  = partial(compute_thresholds,
	                          random_state=42,
	                          n_jobs=1)

ar = AutoReject(thresh_func=thresh_func, verbose='tqdm')

index = np.random.choice(np.arange(len(epochs)),
                         size=int(np.floor(len(epochs) * 0.1)),
                         replace=False)
ar.fit(epochs[index])

epochs_clean = ar.transform(epochs)

print("{:.2f}% epochs rejected (N={})".format(
      epochs_clean.drop_log_stats(), len(epochs_clean)))


data = epochs_clean.get_data() # load your python array, preprocessed





data = data[:,np.array([8, 31, 229]),:3000]
data = np.transpose(data, (0, 2, 1))
assert(data.ndim==3 and data.shape[1:]==(3000,3))

clf = Classifier()
# clf.download_weights()  # skip this if you already downloaded them.
# https://www.dropbox.com/s/otm6t0u2tmbj7sd/cnn.hdf5?dl=1
# https://www.dropbox.com/s/t6n9x9pvt5tlvj8/rnn.hdf5?dl=1
clf.load_cnn_model('./weights/cnn.hdf5')
clf.load_rnn_model('./weights/rnn.hdf5')
preds = clf.predict(data, classes=True)