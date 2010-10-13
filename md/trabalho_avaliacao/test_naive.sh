#!/bin/bash
echo Running
algo=naive
java -cp /home/pedro/Downloads/weka-3-6-3/build/classes/ weka.classifiers.bayes.NaiveBayes -i -l models/$algo$i -T data/test_$i.arff &> log_$algo_test$i.txt
more log_$algo_test$i.txt
