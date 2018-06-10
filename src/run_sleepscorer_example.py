# https://github.com/skjerns/AutoSleepScorer
import os
import numpy as np
import matplotlib.pyplot as plt
from sleepscorer.tools import download, show_sample_hypnogram, plot_hypnogram
import sleepscorer

if not os.path.isfile('../data/derived/sample-psg.edf'):
    print('A sample file from the EDFx database will be loaded...')
    download('https://physionet.nlm.nih.gov/pn4/sleep-edfx/SC4001E0-PSG.edf', '../data/derived/sample-psg.edf')
    download('https://pastebin.com/raw/jbzz16wP', '../data/derived/sample-psg.hypnogram.csv') 
    
sleepdata = sleepscorer.sleeploader.SleepData('../data/derived/sample-psg.edf', start = 2880000, stop = 5400000, channels={'EEG':'EEG Fpz-Cz', 'EMG':'EMG submental', 'EOG':'EOG horizontal'}, preload=False)
data = sleepdata.get_data()
assert(data.ndim==3 and data.shape[1:]==(3000,3))
clf = sleepscorer.Classifier()
# clf.download_weights()  # skip this if you already downloaded them.
# https://www.dropbox.com/s/otm6t0u2tmbj7sd/cnn.hdf5?dl=1
# https://www.dropbox.com/s/t6n9x9pvt5tlvj8/rnn.hdf5?dl=1
clf.load_cnn_model('../data/derived/weights/cnn.hdf5')
clf.load_rnn_model('../data/derived/weights/rnn.hdf5')
preds = clf.predict(data, classes=True)

# Plot the hypnogram
show_sample_hypnogram('../data/derived/sample-psg.hypnogram.csv')  
plot_hypnogram(preds)
plt.show()