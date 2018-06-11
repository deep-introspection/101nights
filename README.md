# #101nights
Scripts for the #101nights project, during the first [Brainhack Network](http://brainhack-networks.com/program).

[Website](http://www.dreamsessions.org/101nights.html) | [Data](https://www.dropbox.com/sh/bnzgspyjutjyjcq/AAD63mR1tLYxtytRVQiTCMLDa?dl=0) | [Slack channel](https://brainhack.slack.com/messages/101nights/) (to join the Brainhack Slack click [here](https://brainhack-slack-invite.herokuapp.com/))

<img src="http://www.dreamsessions.org/images/101nights/Panorama.jpg">

## Backlog
<img src="https://img.shields.io/badge/1-Ready%3F-red.svg?longCache=true&style=for-the-badge">

:heavy_check_mark: read the brain waves data ([MNE Python](https://github.com/mne-tools/mne-python))

:heavy_check_mark: extract and format all the dreams (dream.txt)

:heavy_check_mark: extract and format all daily logs (daily-logs.txt)

:heavy_check_mark: read XMLs for the "incepted" messages

<img src="https://img.shields.io/badge/2-Steady...-orange.svg?longCache=true&style=for-the-badge">

:heavy_check_mark: artifacts rejection & sensor interpolation ([autoreject](http://autoreject.github.io/))

:heavy_check_mark: parse triggers from the EEG recordings

:heavy_check_mark: semantic modeling of dreams ([word2vec](https://radimrehurek.com/gensim/models/word2vec.html))

:heavy_check_mark: sleep stages inference ([AutoSleepScorer](https://github.com/skjerns/AutoSleepScorer))

<img src="https://img.shields.io/badge/3-Go!-green.svg?longCache=true&style=for-the-badge">

:heavy_check_mark: hierarchical block (cluster-topic) modeling of dreams ([abstractology](https://gitlab.com/solstag/abstractology/))

:heavy_check_mark: test effect of "incepted" messages on the content of dreams (tips: use [cosine distance](https://www.researchgate.net/post/What_is_the_best_way_to_measure_text_similarities_based_on_word2vec_word_embeddings) or [n_similarity](https://tedboy.github.io/nlps/generated/generated/gensim.models.Word2Vec.n_similarity.html))

:heavy_check_mark: extract functional brain networks at [scalp level](https://www.martinos.org/mne/stable/auto_examples/connectivity/plot_sensor_connectivity.html#sphx-glr-auto-examples-connectivity-plot-sensor-connectivity-py)

:soon: [get to the source level](http://www.martinos.org/mne/stable/manual/cookbook.html) using MRI data

:heavy_minus_sign: ...
