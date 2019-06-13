# Hourly Crpytocurrency Price Predictor

The main bulk of the code was wriiten by Sentdex however I have added the predict.py file, tweaked the code in general and changed the input files which has collectively changed the AI's functionality from predicting minutes out to predicting hours out. The RNN has been trained rigourously ensuring there is no overfitting, and the result is a model that can predict the price of Bitcoin 3 hours into the future with an accuracy of 60%.

You can load any 4 different cryptocurrency csv files that contain historical data in the the same format as what is shown in the csv files on this repository.

Currently 60% accuracy is achieved by using a sequence length of 180 and a future prediction length of 3.

You can change the RATIO_TO_PREDICT variable to alter the crpytocurrency you would like to predict.

This RNN uses the price and volume to make its predictions. However it does not only use the price and volume of the crpyto we are predicting, but of 3 other cryptos too.
