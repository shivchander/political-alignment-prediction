# Test Plan

## Overall Test Plan

We plan to test our application by allocating some data points in the master dataset as test data points. To get the best results we choose the data points randomly in different ratios multiple times and we plan to do this in 5 phases. We used a Kaggle dataset that has about 500 politicians with their classes - democrats and republicans. Then another dataset was used that didn’t have anyone from these 500 politicians to test the model. In each phase a confusion matrix was used to compare the TP(True Positive), TN(True Negative), FP(False Positive), FN(False Negative) values 

## Test Case Descriptions

1. Normalization Test
    1. This test is designed to determine whether the normalization procedure on the data will proceed identically to the tweets
    2. This test will randomly select a tweet from the training data, send it through the normalization process, and compare it to the output from normalizing all of the training data together. 
    3. The inputs are the list of training data and one element of those, randomly selected.
    4. The output is the normalized tweets; the randomly selected tweet should be identical in each case.
    5. Normal
    6. Whitebox
    7. Functional
    8. Unit
    
2. Padding Test
    1. This test is designed to determine whether the padding tweets to a specific length affects the perfomance
    2. This test will take a normal tweet, send it through the padding and reshaping process.
    3. The inputs are tweets shorter and longer than the predetermined padding length
    4. Boundary
    5. Blackbox
    6. Functional
    7. Unit
    
3. Reshaping Test
    1. This test is designed to determine whether the reshaping procedure correctly maps input values to their corresponding output spaces.
    2. This test will take a manually defined tweet, send it through the reshaper, and make sure that all values are mapped to their correct positions.
    3. Normal
    4. Blackbox
    5. Functional
    6. Unit
 
4. Model Encoding Test
    1. This test is designed to determine whether the model encoding/decoding process correctly saves the weights, layer configuration, and parameters and loads the model into memory accurately.
    2. The test will take a trained model, encode it, save it to disk, retrieve and decode that model, and then classify all testing data.
    3. The input is the trained model and the testing data.
    4. The output is two lists of classified outputs: the trained model's classifications of the testing set before and after the encoding/decoding process.
    5. Normal
    6. Whitebox
    7. Functional
    8. Integration
    
5. Classification Benchmark
    1. This test is designed to determine whether the classification process can be performed quickly enough to be run in near-real-time.
    2. The test will take a list of tweets and, for each one, preprocess it, shape it for ingestion, and classify it. The test will be run across the entire set of tweets and the time needed will be averaged.
    3. The input is the entire dataset.
    4. The output is the average time to preprocess and classify each test, which should take less time than is necessary to generate another.
    5. Normal
    6. Blackbox
    7. Performance
    8. Integration

## Test Case Matrix

|    | Normal/Abnormal | Blackbox/Whitebox | Functional/Performance | Unit/Integration |
|----|:---------------:|:-----------------:|:----------------------:|:----------------:|
| NT |      Normal     |      Whitebox     |       Functional       |       Unit       |
| PT |     Boundary    |      Blackbox     |       Functional       |       Unit       |
| RT |     Boundary    |      Blackbox     |       Functional       |       Unit       |
| MT |      Normal     |      Whitebox     |       Functional       |    Integration   |
| CB |      Normal     |      Blackbox     |      Performance       |    Integration   |