# -*- coding: utf-8 -*-
"""Stock Market Sentiment Analysis Tutorial.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1eybhmYSfKFY-YPvknYzP90Q0t7MIziPN
"""

#Description: This program predicts if the stock price of a company will increase or decrease
#             based on top news headlines.

pip install vaderSentiment

#Import the libraries
import pandas as pd
import numpy as np
from textblob import TextBlob
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

#Load the data
from google.colab import files
files.upload()

#Store the data into variables
df1 = pd.read_csv('Dow_Jones_Industrial_Average_News.csv')
df2 = pd.read_csv('Dow_Jones_Industrial_Average_Stock.csv')

#Show the first 3 rows of data for df1
df1.head(3)

#Get the number of rows and columns
df1.shape

#Print the first 3 rows of data for df2
df2.head(3)

#get the number of rows and columns
df2.shape

#Merge the data set on the date field
merge = df1.merge(df2, how='inner', on='Date')

#Show the merged data set
merge

#Combine the top news headlines
headlines = []

for row in range(0, len(merge.index)):
  headlines.append(' '.join( str(x) for x in merge.iloc[row, 2:27]))

#print a sample of the combined headlines
headlines[0]

#Clean the data
clean_headlines = []

for i in range(0, len(headlines)):
  clean_headlines.append(re.sub("b[(')]", '', headlines[i])) # remove b'
  clean_headlines[i] = re.sub('b[(")]', '', clean_headlines[i]) # remove b"
  clean_headlines[i] = re.sub("\'", '', clean_headlines[i]) #remove \'

#Show the combined cleaned headlines
clean_headlines[20]

#Add the clean headlines to the merge data set
merge['Combined_News'] = clean_headlines

#Show the new column
merge['Combined_News'][0]

#Show the first 3 rows of the merge data set
merge.head(3)

#Create a function to get the subjectivity
def getSubjectivity(text):
  return TextBlob(text).sentiment.subjectivity

#Create a function to get the polarity
def getPolarity(text):
  return TextBlob(text).sentiment.polarity

#Create two new columns 'Subjectivity' and 'Polarity'
merge['Subjectivity'] = merge['Combined_News'].apply(getSubjectivity)
merge['Polarity'] = merge['Combined_News'].apply(getPolarity)

#Show the new columns in the merge data set
merge.head(3)

#Create a function to get the sentiment scores
def getSIA(text):
  sia = SentimentIntensityAnalyzer()
  sentiment = sia.polarity_scores(text)
  return sentiment

#Get the sentiment scores for each day
compound = []
neg = []
pos = []
neu = []
SIA = 0

for i in range(0, len(merge['Combined_News'])):
  SIA = getSIA(merge['Combined_News'][i])
  compound.append(SIA['compound'])
  neg.append(SIA['neg'])
  neu.append(SIA['neu'])
  pos.append(SIA['pos'])

#Store the sentiment scores in the merge data set
merge['Compound'] = compound
merge['Negative'] = neg
merge['Neutral'] = neu
merge['Positive'] = pos

#Show the merge data
merge.head(3)

#Create a list of columns to keep
keep_columns = ['Open', 'High', 'Low', 'Volume', 'Subjectivity', 'Polarity', 'Compound', 'Negative', 'Neutral', 'Positive', 'Label']

df = merge[keep_columns]
df

#Create the feature data set
X = df
X = np.array(X.drop(['Label'], 1))

#Create the target data set
y = np.array(df['Label'])

#Split the data into 80% training and 20% testing data sets
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

#Create and train the model
model = LinearDiscriminantAnalysis().fit(x_train, y_train)

#Show the models predictions
predictions = model.predict(x_test)
predictions

y_test

#Show the model metrics
print(classification_report(y_test, predictions))

!wget -nc https://raw.githubusercontent.com/brpy/colab-pdf/master/colab_pdf.py
from colab_pdf import colab_pdf
colab_pdf('Stock Market Sentiment Analysis Tutorial.ipynb')

