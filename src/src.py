"""_Sentiment Analysis_
@author:
    Jakob Balkovec

@date:
    November 28th, 2023

@version:
    1.0

@license:
    This code is licensed under the MIT License.

@file:
    src.py

@description:
    This script implements a sentiment analysis algorithm that determines the sentiment 
    polarity (positive, negative, or neutral) of textual data. 
    
@usage:
    Run this script with the necessary dependencies installed and provide the text data to be analyzed. 
    The algorithm will output the sentiment polarity score for each input.
    
@note:
Python 3.11.4 env
"""

"""__imports__"""
import string
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

import logging

"""__constants__"""
LOGGER_NAME: str = "File: src.py"

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('logs/src.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
  
def strip_characters(sentence: str) -> str:
  """__doc__
  Remove special characters, punctuation, and unnecessary whitespaces from a sentence.
  """
  sentence = re.sub(r"[^a-zA-Z0-9\s]", "", sentence)
  sentence = sentence.translate(str.maketrans('', '', string.punctuation))
  sentence = " ".join(sentence.split())
  
  logger.info(f"[sentence stripped of special characters]: {sentence}")
  return sentence.lower()

def tokenize(sentence: str) -> list:
  """__doc__
  Tokenize a sentence into a list of words.
  """
  placeholder = nltk.word_tokenize(sentence)
  logger.info(f"[sentence tokenized]: {placeholder}")
  return placeholder

def stem(sentence: list) -> list:
  """__doc__
  Stem a sentence.
  """
  stemmer = nltk.stem.PorterStemmer()
  placeholder = [stemmer.stem(word) for word in sentence]
  logger.info(f"[sentence stemmed]: {placeholder}")
  return placeholder

def preprocess(sentence: str) -> list:
  """__doc__
  Preprocess a sentence.
  """
  sentence = strip_characters(sentence)
  sentence = tokenize(sentence)
  sentence = stem(sentence)
  
  logger.info(f"[sentence preprocessed]: {sentence}")
  return sentence

def get_polarity(sentence: list) -> float:
  """
  Calculate the polarity score of a given sentence.

  Args:
    sentence (str): The input sentence for sentiment analysis.

  Returns:
    float: The polarity score of the sentence.
  """
  sentence: str = " ".join(sentence)
  
  sid = SentimentIntensityAnalyzer()
  sentiment_scores = sid.polarity_scores(sentence)
  
  logger.info(f"[sentence polarity score calculated]: {sentiment_scores['compound']}")
  return sentiment_scores['compound']

def get_subjectivity(sentence: list) -> float:
    """
    Calculate the subjectivity of a given sentence.

    Parameters:
    sentence (str): The input sentence for which subjectivity needs to be calculated.

    Returns:
    float: The subjectivity score of the sentence, ranging from 0.0 to 1.0.
      A score closer to 0.0 indicates objective content, while a score closer to 1.0 indicates subjective content.
    """
    sentence: str = " ".join(sentence)
    blob = TextBlob(sentence)
    logger.info(f"[sentence subjectivity score calculated]: {blob.sentiment.subjectivity}")
    return blob.sentiment.subjectivity

def get_polarity_category(polarity: float) -> str:
  """
  Returns the polarity category based on the given polarity value.

  Parameters:
  polarity (float): The polarity value to categorize.

  Returns:
  str: The polarity category.

  """
  if polarity > 0.5:
    return "Very Positive"
  elif polarity > 0.0:
    return "Positive"
  elif polarity == 0.0:
    return "Neutral"
  elif polarity >= -0.5:
    return "Slightly Negative"
  else:
    return "Very Negative"

def get_subjectivity_category(subjectivity: float) -> str:
  """
  Determines the category of subjectivity based on the given subjectivity score.

  Args:
    subjectivity (float): The subjectivity score ranging from 0 to 1.

  Returns:
    str: The category of subjectivity, either "Subjective" or "Objective".
  """
  if subjectivity >= 0.5:
    return "Subjective"
  else:
    return "Objective"
      
def get_sentiment(sentence: str) -> dict:
  """
  Calculate the sentiment of a given sentence.

  Args:
    sentence (str): The input sentence for sentiment analysis.

  Returns:
    dict: A dictionary containing the sentiment analysis results, including:
      - sentence: The input sentence.
      - polarity_score: The polarity score of the sentence.
      - subjectivity_score: The subjectivity score of the sentence.
      - polarity: The polarity category of the sentence.
      - subjectivity: The subjectivity category of the sentence.
  """
  processed_sentence = preprocess(sentence)
  polarity = get_polarity(processed_sentence)
  subjectivity = get_subjectivity(processed_sentence)

  return {
    "Sentiment": {
      "sentence": sentence,
      "polarity_score": polarity,
      "subjectivity_score": subjectivity,
      "polarity": get_polarity_category(polarity),
      "subjectivity": get_subjectivity_category(subjectivity)
    }  }

