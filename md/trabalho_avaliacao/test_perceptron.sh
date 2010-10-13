#!/bin/bash
echo Running
java -cp /home/pedro/Downloads/weka-3-6-3/build/classes/ weka.classifiers.functions.MultilayerPerceptron -i -l models/perceptron$i -T data/test_$i.arff &> log_perceptron_test$i.txt
more log_perceptron_test$i.txt
