echo Running
java -cp /home/pedro//Downloads/weka-3-6-3/build/classes/ weka.classifiers.functions.MultilayerPerceptron -L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H 80 -d models/perceptron$i -t data/train_$i.arff  -no-cv -i &> log_perceptron_train$i.txt
less log_perceptron_train$i.txt
