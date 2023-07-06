# **ECG HEARTBEAT CLASSIFICATION WITH ML - Mortara**
by Erica Brisigotti, Ekaterina Chueva, Sofia Pacheco Garcia, Nadillia Sahputra

This project is part of the Laboratory of Computational Physics (mod. B) class from the Physics of Data Master's Degree, held at the University of Padova during Academic Year 2022-2023. The project was supervised by professors Alberto Zucchetta, Marco Zanetti and teaching assistant Federico Agostini.

The current work is motivated by the fact that cardiologists could spend up to several weeks labelling the electrocardiogram signal (ECGs), but the machine learning can help with this task and therefore save the doctors’ time. The goal of the project was to implement a machine learning algorithm that is able to classify heartbeats to normal and abnormal ones (corresponding to different cardio diseases) using given ECGs.

The target dataset is 450 Holter ECGs collected in the past decade by the Cardiology Department of the University of Padova. We refer to this dataset as ‘Mortara dataset’. Each ECG is a 12 leads, 24h recording of a single patient. Unfortunately, we could not use any of the recordings for training a machine learning model, because it has no labels and we would like to develop a supervised ML algorithm.

We found a similar dataset to use as a training one:  [PhysioNet St Petersburg INCART 12-lead Arrhythmia Database dataset](https://physionet.org/content/incartdb/1.0.0/). This database consists of 75 annotated recordings extracted from 32 Holter records. Each record is 30 minutes long and contains 12 standard leads, each sampled at 257 Hz, with reference annotation files, totalling over 175000 beat annotations in all.

To summarize, we use the latter dataset to develop an overall analysis algorithm and save a pre-trained ML model. The presence of labels in this dataset allows us to find the accuracy of the developed analysis. Then we follow the same steps for the former (Mortara) dataset and classify heartbeats using saved ML model.

## **The files in these directory are**:
1) ECG_Physionet.ipynb: a jupyter notebook with development of the signal preprocessing, heartbeat detection and segmentation, machine learning model.
2) ECG_Mortara.ipynb/ ECG_Mortara_Extended.ipynb: same analysis as in the previous file, but applied to Mortara dataset using the saved ML model.
3) ECG_Doctor.ipynb: jupyter notebook for visualizing the results of application of ML model to the Mortara dataset. It consists a Plotly Dash interface.
4) xgboost_param_nwin4.csv: a csv file with saved ML parameters after GridSearch
5) multi_maxdepth5_nwindow3.json: a JSON file with pre-trained on Physionet dataset ML model

## **Content of the project**
Here we give a brief description of the project content to give an idea of the analysis. For in depth understanding it is necessary to consult the ECG_Physionet.ipynb file.

### 1) Preprocessing of the data

In order to preprocess the data, we apply several filters: band-pass filter in frequency in Fast Fourier Transform, additional noise filtering with Discrete Wavelet Transform and finally we also eliminate a baseline wander of the signal. In order to standardize the signal, after all the filtering parts we transform it to the one with mean=0 and std=1.

### 2) R-peaks detection

Since we do not have any annotations (labels) in the Mortara dataset, we had to develop an independent algorithm for detecting the heartbeats (which does not rely on any labels-related information). It was done with algorithm based on fitting the signal with parabola. Then, since we have 12 leads and the “real” peak should be present in the majority of them, we confirm the peak as detected only if the peak is presented in more than a certain number of leads (we set a threshold).

We find the balanced accuracy of the R-peaks detection algorithm for the Physionet dataset: 95%.

### 3) Segmentation of the signal
We would like to separate each heartbeat and later compose a feature vector for each. For this we use the previously found R-peaks and the knowledge about the duration of the heartbeat.

### 4) Extraction of features

Before going directly to feature extraction, we discard heartbeats with extremely anomalous characteristics, since it is either the noise or the algorithm mistake and we do not want to analyse and process this further.

The features that we extract (all the positions are relative to each heartbeat):

a) discrete wavelet transform coefficients

b) the start and end of the QRS complex

c) the (real) position and height of the R peak

d) the difference (err) between the two estimates of the position of the R peak

e) the value and position of the maximum of the heartbeat 

d) the value and position of the minimum of the heartbeat

f) the positive and negative integral of the heartbeat 

g) the positive and negative integral of the QRS complex 

h) the start and end of the P peak 

i) the position and height of the P peak

j) the positive and negative integral of the P peak 

k) the start and end of the T peak 

l) the position and height of the T peak

m) the positive and negative integral of the T peak

After we construct a feature matrix that we further use for ML.

### 5) Machine learning part

We select the most popular (> 1%)  classes in the Physionet dataset. These end up consisting of the normal heartbeats (labelled as N) and heartbeats with one of three anomalies: atrial premature contraction (A), right bundle branch block beat (R), premature ventricular contraction (V). All other we merge into one ‘other’ class.
We then implement a XGBoost multi classification model, pre-train it and save. 

The balanced accuracy appeared to be around 98%. Furthermore, our model has a low false positive  (meaning that normal heartbeats are classified as abnormal) rate: 0.3%, which is crucial for the proposed goal of the project.

### 6) Test on Mortara dataset

Finally, we test our algorithm on Mortara datasets and visualize the result of classification along with initial signal for doctor’s check.
