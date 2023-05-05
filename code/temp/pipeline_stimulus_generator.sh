#!/bin/bash -x

# Generate full stimulus set for each NA-task
python stimulus_generator_templates.py --natask subjrel -seed 1 -n 256 > ../stimuli/English_subjrel.txt
python stimulus_generator_templates.py --natask objrel -seed 1 -n 256 > ../stimuli/English_objrel.txt
python stimulus_generator_templates.py --natask objrel_nounpp -seed 1 -n 64 > ../stimuli/English_objrel_nounpp.txt
python stimulus_generator_templates.py --natask embedding_mental_SR -seed 1 -n 256 > ../stimuli/English_embedding_mental_SR.txt
python stimulus_generator_templates.py --natask embedding_mental -seed 1 -n 64 > ../stimuli/English_embedding_mental.txt
python stimulus_generator_templates.py --natask embedding_mental_2LRs -seed 1 -n 16 > ../stimuli/English_embedding_mental_2LRs.txt
python stimulus_generator_templates.py --natask objrel_pronoun -seed 1 -n 256 > ../stimuli/English_objrel_pronoun.txt
python stimulus_generator_templates.py --natask SC_OR -seed 1 -n 256 > ../stimuli/English_SC_OR.txt