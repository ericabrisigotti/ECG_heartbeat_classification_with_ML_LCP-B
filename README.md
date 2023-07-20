# **ECG HEARTBEAT CLASSIFICATION WITH ML**
by Erica Brisigotti, Ekaterina Chueva, Sofia Pacheco Garcia, Nadillia Sahputra

This project is part of the Laboratory of Computational Physics (mod. B) class from the Physics of Data Master's Degree, held at the University of Padova during Academic Year 2022-2023. The project was supervised by professors Alberto Zucchetta and Marco Zanetti, and teaching assistant Federico Agostini.

The current work is motivated by the fact that cardiologists can spend up to several weeks labeling the electrocardiogram signal (ECGs): machine learning can take care of this task and help save doctors’ time and improve efficiency in the healthcare system. 

The goal of the project is to implement a machine learning algorithm that is able to classify heartbeats into normal and abnormal ones (corresponding to different cardio diseases) using given ECGs. The target dataset is 450 Holter ECGs collected in the past decade by the Cardiology Department of the University of Padova. We refer to this dataset as ‘Mortara dataset’. Each ECG is a 12 leads, 24h recording of a single patient. Unfortunately, we could not use any of the recordings for training a machine learning model, because it has no labels and we would like to develop a supervised ML algorithm.

We found a similar dataset to use as a training one:  [PhysioNet St Petersburg INCART 12-lead Arrhythmia Database dataset](https://physionet.org/content/incartdb/1.0.0/). This database consists of 75 annotated recordings extracted from 32 Holter records. Each record is 30 minutes long and contains 12 standard leads, each sampled at 257 Hz, with reference annotation files, totaling over 175000 beat annotations in all.

To summarize, we firsly use the latter dataset to develop an overall analysis algorithm and save a pre-trained ML model. The presence of labels in this dataset allows us to estimate the accuracy of the developed analysis. We then follow the same steps for the former (Mortara) dataset and classify heartbeats using the saved ML model.

## **The files in this directory are**:
1) <code>ECG_Physionet.ipynb</code>: a jupyter notebook with development of the signal preprocessing, heartbeat detection and segmentation, and machine learning model.
2) <code>ECG_Mortara.ipynb</code>/<code>ECG_Mortara_Extended.ipynb</code>: same analysis as in the previous file, but applied to 2 halves of a Mortara dataset using the saved ML model.
3) <code>ECG_Doctor.ipynb</code>: a jupyter notebook for visualizing the predictions made by the ML model on the Mortara dataset. It consists of a Plotly Dash interface.
4) <code>xgboost_param_nwin4.csv</code>: a CSV file with saved (optimal) ML parameters after GridSearch
5) <code>multi_maxdepth5_nwindow3.json</code>: a JSON file with pre-trained on Physionet dataset ML model
6) <code>everything.csv</code>/<code>everything_extended.csv</code>: are CSV files containing all the information about the Mortara/Mortara Extended heartbeats including the ML classification results. This is the input file for ECG_Doctor.ipnyb


## **Content of the project**
Here we give a brief description of the project content to give an idea of the analysis. For an in-depth understanding, it is necessary to consult the <code>ECG_Physionet.ipynb</code> file.

### 1) Preprocessing of the data

To preprocess the data, we apply several filters: band-pass filter in frequency in Fast Fourier Transform, additional noise filtering with Discrete Wavelet Transform, and lastly, we filter out the baseline wander of the signal. We then standardize the signal by transforming it to the one with mean=0 and std=1.

### 2) R-peaks detection

Since we do not have any annotations (labels) in the Mortara dataset, we had to develop an independent algorithm for detecting the heartbeats (which does not rely on any labels-related information). Peak identification was implemented with an algorithm based on the minimization of the error 
 between the parabola fit of consecutive signal windows and the actual signal for each lead. Then, since we have 12 leads and the “real” peak should be present in the majority of them, we confirm the peak as detected only if the peak is presented in more than a certain number of leads (we set a threshold).

We calculate the balanced accuracy of the R-peaks detection algorithm for the Physionet dataset: 95%.

### 3) Segmentation of the signal
We would like to separate each heartbeat with a variable window-size algorithm, to later compose a feature vector for each. For this, we use the previously found R-peaks and the known proportions between the duration of phases of the heartbeat.

### 4) Extraction of features

Before going directly to feature extraction, we discard heartbeats with extremely anomalous characteristics, since it is either the noise or the algorithm mistake and we do not want to analyze and process them further. Such selection is based on the distributions of RR length, mean signal over the heartbeat, and standard deviation of the signal over the heartbeat.

The features that we extract:

- discrete wavelet transform coefficients

- the start and end of the QRS complex

- the (real) position and height of the R peak

- the difference (err) between the two estimates of the position of the R peak

- the value and position of the maximum of the heartbeat 

- the value and position of the minimum of the heartbeat

- the positive and negative integral of the heartbeat 

- the positive and negative integral of the QRS complex 

- the start and end of the P peak 

- the position and height of the P peak

- the positive and negative integral of the P peak 

- the start and end of the T peak 

- the position and height of the T peak

- the positive and negative integral of the T peak

Such features are all relative to the heartbeat and converted from indexes to seconds when appropriate. We collected them in a matrix that is used as the input of out ML algorithm.

### 5) Machine learning part

We select the most popular (> 1%)  classes in the Physionet dataset. These end up consisting of normal heartbeats (labeled as N) and heartbeats with one of three anomalies: atrial premature contraction (A), right bundle branch block beat (R), and premature ventricular contraction (V). All others we merge into one ‘other’ class.
We then implement an XGBoost multi-classification model, which was pre-trained with the parameters obtained from GridSearch pre-train saved. 

The balanced accuracy is estimated to be around 98%. Furthermore, our model has a low false positive (normal heartbeats that are classified as abnormal) rate: 0.3%, which is crucial for the proposed goal of the project.

### 6) Test on Mortara dataset

Finally, we test our algorithm on Mortara datasets and visualize the result of classification along with the signal for the doctor’s check.
