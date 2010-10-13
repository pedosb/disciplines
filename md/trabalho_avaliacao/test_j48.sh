#!/bin/bash
echo Running
java -cp /home/pedro/Downloads/weka-3-6-3/build/classes/ weka.classifiers.trees.J48 -i -l models/j48$i -T data/test_$i.arff &> log_j48_test$i.txt
more log_j48_test$i.txt
