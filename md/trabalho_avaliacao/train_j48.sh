echo Running
java -cp /home/pedro//Downloads/weka-3-6-3/build/classes/ weka.classifiers.trees.J48 -C 0.25 -M 20 -d models/j48$i -t data/train_$i.arff -no-cv -i &> log_j48_train$i.txt
less log_j48_train$i.txt
