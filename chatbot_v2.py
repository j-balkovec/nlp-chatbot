"""_Sentiment Analysis ChatBot_
@author:
    Jakob Balkovec

@date:
    December 16th, 2023

@version:
    2.0

@license:
    This code is licensed under the MIT License.

@file:
    chatbot_v2.py

@description:
    This script implements a sentiment analysis algorithm that determines the sentiment 
    polarity (positive, negative, or neutral) of textual data. 
    The data is displayed in a neat looking GUI made with the customtkinter module.
    
@usage:
    Run this script with the necessary dependencies installed and provide the text data to be analyzed. 
    The algorithm will output the sentiment polarity score for each input.
    
@note:
Python 3.11.2 64-bit env to run customtkinter module
"""

"""__imports__"""
import json
import tkinter as tk
from src.src import get_sentiment
from tkinter import *
import customtkinter as ctk

import logging

"""__constants__"""
WINDOW_SIZE: str = "600x400"
WINDOW_TITLE: str = "Sentiment Analysis Chatbot"

FONT_FAMILY: str = "Menlo"
FONT_SIZE: int = 12

UNI_WIDTH: int = 500 #Universal Width
HEIGHT: int = 220

ENTER_KEY: str = "<Return>"

"""__padding_constants__"""
CTK_ENTRY_X_PADDING: int = 50
CTK_ENTRY_Y_PADDING: int = 50

CTK_TEXTBOX_X_PADDING: int = 20
CTK_TEXTBOX_Y_PADDING: int = 20

CTK_BUTTON_X_PADDING: int = 50
CTK_BUTTON_Y_PADDING: int = 10

CTK_LABEL_Y_PADDING: int = 20

"""__logging_constants__"""
CLASS_LOGGER: str = "GUI Class"
EXTERNAL_LOGGER: str = "File: chatbot_v2.py"

class SentimentChatbotGUI(ctk.CTkFrame):
  """
  A GUI class for a Sentiment Analysis Chatbot.

  Attributes:
    master (ctk.CTkFrame): The main frame of the GUI.
    input_entry (ctk.CTkEntry): The entry field for user input.
    output_text (ctk.CTkTextbox): The text box for displaying chatbot responses.
    analyze_button (ctk.CTkButton): The button for analyzing user input.
    exit_button (ctk.CTkButton): The button for exiting the chatbot.
  """
  
  """__logger__
  Initializes the logger.
  """
  logger = logging.getLogger(CLASS_LOGGER)
  logger.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  file_handler = logging.FileHandler('logs/chatbot.log')
  file_handler.setFormatter(formatter)
  logger.addHandler(file_handler)
  
  def __init__(self, root):
    """
    Initializes the SentimentChatbotGUI.

    Args:
      root: The root window of the GUI.
    """
    root.geometry(WINDOW_SIZE)
    root.title(WINDOW_TITLE)
    
    """__frame__
    Initializes the main frame of the GUI.
    """
    self.master = ctk.CTkFrame(root)
    self.master.pack(expand=True, fill="both")
    self.logger.info("[frame initialized]")
    
    """__font__
    Initializes the font for the GUI.
    """
    my_font = ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZE)
    self.logger.info(f"[font set to {FONT_FAMILY} {FONT_SIZE}]")
    
    """__entry__
    Initializes the entry field for user input.
    """
    self.input_entry = ctk.CTkEntry(self.master, placeholder_text="Message Chatbot...", width=UNI_WIDTH, font=my_font)
    self.input_entry.pack(side=tk.BOTTOM, padx=(CTK_ENTRY_X_PADDING, CTK_ENTRY_X_PADDING), pady=(0, CTK_ENTRY_Y_PADDING), fill=tk.X)
    self.logger.info(f"[entry field initialized, width: {UNI_WIDTH}, height: {HEIGHT}]")
    self.logger.debug(f"[entry field x padding: {CTK_ENTRY_X_PADDING}, y padding: {CTK_ENTRY_Y_PADDING}]")
    
    """__textbox__
    Initializes the text box for displaying chatbot responses.
    """
    self.output_text = ctk.CTkTextbox(self.master, width=UNI_WIDTH, height=HEIGHT, font=my_font)
    self.output_text.pack(side=tk.TOP, padx=(CTK_TEXTBOX_X_PADDING, CTK_TEXTBOX_X_PADDING), pady=(CTK_TEXTBOX_Y_PADDING, 0), fill=tk.Y)
    self.logger.info(f"[text box initialized, width: {UNI_WIDTH}, height: {HEIGHT}]")
    self.logger.debug(f"[text box x padding: {CTK_TEXTBOX_X_PADDING}, y padding: {CTK_TEXTBOX_Y_PADDING}]")
    
    """__label__
    Made by label.
    """
    self.made_by_label = ctk.CTkLabel(self.master, text="Made by JB", font=my_font, fg_color="transparent", text_color="lightgray")
    self.made_by_label.pack(side=tk.BOTTOM, padx=(0, 0), pady=(0, CTK_LABEL_Y_PADDING), fill=tk.Y)
    
    """__buttons__
    Initializes the buttons for analyzing user input.
    """
    self.analyze_button = ctk.CTkButton(self.master, text="Analyze", command=self.analyze_sentence, font=my_font)
    self.analyze_button.pack(side=tk.LEFT, padx=(CTK_BUTTON_X_PADDING, CTK_BUTTON_Y_PADDING), pady=5)
    self.logger.info("[analyze button initialized, callback \"self.analyze_sentence\"]")
    self.logger.debug(f"[analyze button x padding: {CTK_BUTTON_X_PADDING}, y padding: {CTK_BUTTON_Y_PADDING}]")

    """__buttons__
    Exit button.
    """
    self.exit_button = ctk.CTkButton(self.master, text="Exit", command=root.destroy, font=my_font)
    self.exit_button.pack(side=tk.RIGHT, padx=(CTK_BUTTON_Y_PADDING, CTK_BUTTON_X_PADDING), pady=5)
    self.logger.info("[exit button initialized, callback \"root.destroy\"]")
    self.logger.debug(f"[exit button x padding: {CTK_BUTTON_X_PADDING}, y padding: {CTK_BUTTON_Y_PADDING}]")

    """__bind__
    Binds the ENTER_KEY to the input entry field.
    """
    self.input_entry.bind(ENTER_KEY, lambda event: self.analyze_sentence())

  def analyze_sentence(self):
    """
    Analyzes the user input and displays the chatbot's response.
    """
    sentence = self.input_entry.get()
    self.logger.info(f"[user input fetched: {sentence}]")
    if sentence:
      response = chatbot_response(sentence)
      self.logger.info(f"[chatbot response fetched: {response}]")
      self.output_text.insert(tk.END, f"You: \"{sentence}\"\nChatbot: {response}\n\n")
      self.output_text.yview(tk.END)
      self.input_entry.delete(0, tk.END)

    self.logger.info("[user input failed to fetch]")
    return
  
"""__logger__
External Logger
"""
logger = logging.getLogger(EXTERNAL_LOGGER)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('logs/chatbot.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def chatbot_response(sentence: str) -> str:
  """
  Generates a response from the chatbot based on the given sentence.

  Args:
    sentence (str): The input sentence to generate a response for.

  Returns:
    str: The generated response in JSON format.
  """
  data = get_sentiment(sentence)
  json_data = json.dumps(data, indent=4, separators=(',', ': '))
  logger.info(f"[chatbot response fetched]: {json_data}")

  with open("response_log.json", "a") as outfile:
    outfile.write(json_data + "\n")
    
  logger.info(f"[chatbot response logged]: {json_data}")
  return f"\n{json_data}"

def clear_json_log():
  """
  Clears the .json log file.
  """
  with open("logs/response_log.json", "w") as outfile:
    outfile.write("")
  logger.info("[chatbot response-log cleared]")
  return

def clear_log_file():
  """
  Clears the .log file.
  """
  with open("logs/chatbot.log", "w") as outfile:
    outfile.write("")
  logger.info("[chatbot log cleared]")
  return

def print_license():
  """
  Prints the license to the console.
  """
  with open("LICENSE", "r") as outfile:
    print(outfile.read())
  return

def main():
  """
  Main function to initialize and run the sentiment chatbot GUI.

  This function sets the appearance mode and color theme of the GUI,
  creates the root window, and initializes the SentimentChatbotGUI object.
  Finally, it starts the main event loop to handle user interactions.

  Args:
    None

  Returns:
    None
  """
  ctk.set_appearance_mode("dark")
  ctk.set_default_color_theme("green")
  logger.info("[appearance mode set to \"dark\", theme set to \"green\"]")
  
  root = ctk.CTk()
  gui = SentimentChatbotGUI(root)
  logger.info("[root window initialized]")
  
  root.mainloop()

if __name__ == "__main__":
  print_license()
  clear_json_log()
  clear_log_file()
  main()
