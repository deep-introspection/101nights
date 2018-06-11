#! /bin/env python3

# GNU GPLv3+
# https://www.gnu.org/licenses/gpl-3.0.en.html
# Contributors: Ale Abdo <abdo@member.fsf.org>

""" Produces a non-parametric simultaneous hierarchical
    categorization of dreams and their contents, and a
    corresponding interactive visualisation.

    Using the Abstractology module, runs a specially
    crafted hierarchical block model that creates a
    cluster-topic modeling of a corpus.

    The abstractology module is work in progress but can
    be found at:
    https://gitlab.com/solstag/abstractology/
    """

from abstractology import Graphology

# Instantiate the class and load the data, parsing the corpus
a = Graphology('dreamology', text_source='text', gdocvname='night', time='night')
a.load_corpus('dreams.csv', parser='csv', transform={set})
a.register_loaded()

# We're using the "set" transformed column in our analysis
a.set_column('set')
a.set_analysis_path('dreamology/set')
a.register_loaded()

# Create graph and calculate 10 block states
a.create_graphs()
a.calc_nested_blockstate('./auto_abstractology/graphs/dreams+csv-None-set-docvoc-all.gt.xz', runs=10)

# Pick the blockstate with lowest entropy among the 10
entropy = []
for run in range(10):
    a.load_blockstate('./auto_abstractology/graphs/dreams+csv-None-set-docvoc-all.gt-run_{}.nbstate'.format(run))
    entropy.append( (a.state.entropy(), run) )
run = sorted(entropy)[0][1]

# Load the lowest entropy blockstate and plot the block_level_matrix
a.load_blockstate('./auto_abstractology/graphs/dreams+csv-None-set-docvoc-all.gt-run_{}.nbstate'.format(run))
a.blockstate_to_dataframes()
a.plot_block_level_matrix(['doc', 'voc'], norm=['bylevelmax', None],
                          scale=['linear', 'log'])

# Set our sample to be only the incepted dream and replot the matrix
a.set_sample(a.data.loc[a.data.night==50])
a.plot_block_level_matrix(['doc', 'voc'], norm=['bylevelmax', None],
                          scale=['linear', 'log'], desc='inception count')

