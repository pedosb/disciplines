echo Running
algo=naive
java -cp /home/pedro//Downloads/weka-3-6-3/build/classes/ weka.classifiers.bayes.NaiveBayes -d models/$algo$i -t data/train_$i.arff -no-cv -i &> log_$algo_train$i.txt
less log_$algo_train$i.txt
