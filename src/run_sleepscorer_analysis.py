# https://github.com/skjerns/AutoSleepScorer
from sleepscorer import Classifier
from sleepscorer.tools import plot_hypnogram
import mne
import matplotlib.pyplot as plt
import numpy as np
np.random.seed(42)


# Load cleaned epochs
epochs_clean = mne.read_epochs('../data/derived/cleaned_sleep_scorer_epo.fif')
epochs_clean.set_eeg_reference('average', projection=False)
# epochs_clean.plot_sensors(show_names=True)


epochs_clean = mne.io.set_bipolar_reference(epochs_clean,
                                            ['E37'], ['E241'],
                                            # anode, cathode
                                            ch_name=['EOG1'])
epochs_clean.set_channel_types({'EOG1': 'eog'})

epochs_clean = mne.io.set_bipolar_reference(epochs_clean,
                                            ['E18'], ['E238'],
                                            # anode, cathode
                                            ch_name=['EOG2'])
epochs_clean.set_channel_types({'EOG2': 'eog'})

epochs_clean.plot(picks=mne.pick_types(
	epochs_clean.info, emg=False, eeg=False, eog=True,
    stim=False, exclude='bads'))

# Pick a channel for EEG, EMG, EOG
# picks = mne.pick_types(epochs_clean.info, eeg=True, exclude='bads')
epochs_clean.pick_channels(['E16', 'E218', 'EOG'])

epochs_clean.set_channel_types({'E218': 'emg'})
epochs_clean.reorder_channels(['E16', 'E218', 'E31'])

# filter EMG >10Hz
picks = mne.pick_types(epochs_clean.info, emg=True, eeg=False, eog=False,
                       stim=False, exclude='bads')
epochs_clean.filter(10., None, picks=picks,
	                fir_design='firwin', method='iir')

# Format for Sleep Scorer
data = epochs_clean.get_data() # load your python array, preprocessed
data = data[:,:,:3000]
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