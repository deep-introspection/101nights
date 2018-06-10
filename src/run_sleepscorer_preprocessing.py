import mne
from autoreject import AutoReject, compute_thresholds
from functools import partial
import numpy as np
np.random.seed(42)


# Load data
path_to_file = '../data/raw/EEG/Nathalie-78_20171118_123017.mff'
raw = mne.io.read_raw_egi(path_to_file,
                          montage='GSN-HydroCel-256',
                          preload=True)
#raw.crop(tmin=3600, tmax=3600*2)
raw.filter(0.15, None, fir_design='firwin', method='iir')
raw.resample(100, npad='auto')
raw.set_eeg_reference('average', projection=True)


# Create 30s chunks of data
events = mne.event.make_fixed_length_events(
	raw, id=9999, start=0, stop=None, duration=30.0,
	first_samp=True)
epochs = mne.epochs.Epochs(raw, events, tmin=0, tmax=30.0,
                           baseline=None, preload=True)

# Run autoreject
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


# Save cleaned epochs
epochs_clean.save('../data/derived/cleaned_sleep_scorer_epo.fif')
epochs_clean[:11].save('../data/derived/cleaned_subset_sleep_scorer_epo.fif')