## Modelling - Model Selection


### Selecting the best model

Machine learning model building usually follows the path of splitting the data into training and testing sets. Usually, you use the training set to train different models and evaluate the model on the test set to select which is the best one.

However, models that provide the highest accuracy using this approach could just be lucky. For example, training of five different models (DT, LR, SVM, LiR, NN) on detecting spam emails. Say DT gets 66% accuracy, LR gets 75%, SVM gets 50%, LiR gets 85% and NN gets 100% (theoretically). You'd automatically select the NN as the best model right? Yet, it could just be that the NN obtained that accuracy on the test set by chance.

To ensure that the model performance is not a fluke, the data is split into three (training, validation and test sets). The model is trained on the training set, evaluated on the validation set and then the best model is selected and further evaluated on the test set. This is done to prevent the problem of multiple differing performance experienced by ML models.

A more robust approach is splitting into training (60%), validation (20%) and testing (20%), evaluate the model on the validation set, combine the training and validation sets and retrain the model, select the best model and then evaluate on the test set. This ensures that the best performing model was not selected as a fluke but actually performs better than the other models trained.

## Summary of steps in Model Selection

1. Train
2. Test
3. Validation
4. Select best model
5. Combine train and validation sets
6. Evaluate on test data set
