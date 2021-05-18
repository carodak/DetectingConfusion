# Detecting confusion state from EEG signals
## Overview
 In this thesis project, I conducted an experiment and collected EEG brain data from 10 participants to detect the state of confusion. I first processed the EEG data with MATLAB and EEGLAB and then trained machine learning models. I provided the code used to train the learning models and some utility scripts to manipulate the data. The data is not available because it is confidential.
This study led to the acceptance of a scientific paper published at FLAIRS 34 (2021): https://journals.flvc.org/FLAIRS/article/view/128474
 
## Achievements:
To predict whether a person is confused or not, the best model scored 78.6%. 

<p><img src="https://github.com/carodak/DetectingConfusion/blob/main/DetectingConfusion/pictures/2conf.png" width=35% height=35%></p>

To predict the level of confusion (slightly, moderately and very confused), the best model scored 68.0%.

<p><img src="https://github.com/carodak/DetectingConfusion/blob/main/DetectingConfusion/pictures/3conf.png" width=35% height=35%></p>

### Note
Here I have practiced programming following the MVC model, using classes, encapsulation, exceptions and cutting my code into several small methods. So the code can look quite lengthy.
