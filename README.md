# **ECG HEARTBEAT CLASSIFICATION WITH ML - Mortara**
by Erica Brisigotti, Ekaterina Chueva, Sofia Pacheco Garcia, Nadillia Sahputra

This project is part of the Laboratory of Computational Physics (mod. B) class, from the Physics of Data Master's Degree, held at the University of Padova during Academic Year 2022-2023. The project was supervised by professors Alberto Zucchetta, Marco Zanetti and teaching assistant Federico Agostini.

The (ambitious) goal of the project is to test if ML can reliably classify heartbeats from a given ECG dataset. Commercial softwares can perform a preliminary analysis of anormal beats, but a very large fraction of them are false positive anomalies. ML could provide a better identication and classication of the anomalies, signicantly reducing the false-positive ratio.

The ECG dataset consists of 450 Holter ECGs collected in the past decade by the Cardiology Department of the University of Padova. Each ECG is a 12 leads, 24h recording of a single patient. As of executing the project, no ECGs from this datasets provided labels.

We looked outwards for training datasets since we implemented supervised ML techniques. The closest dataset found was the [PhysioNet St Petersburg INCART 12-lead Arrhythmia Database dataset] (https://physionet.org/content/incartdb/1.0.0/). This database consists of 75 annotated recordings extracted from 32 Holter records. Each record is 30 minutes long and contains 12 standard leads, each sampled at 257 Hz, with reference annotation files, totaling over 175000 beat annotations in all. [0]

The ML model was trained in the "ECG_Physionet" file: the trained model was then saved and uploaded in the "ECG_Mortara" file to predict the type of heartbeat.

A Plotly Dash interface (in the "ECG_Doctor" file) was prepared to eventually check the ML predictions with a Cardiologist.
