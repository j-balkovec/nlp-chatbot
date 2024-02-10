"""_Sentiment Analysis ChatBot_
@author:
    Jakob Balkovec

@date:
    December 1st, 2023

@version:
    1.0

@license:
    This code is licensed under the MIT License.

@file:
    chatbot.py

@description:
    This script implements a sentiment analysis algorithm that determines the sentiment 
    polarity (positive, negative, or neutral) of textual data. 
    The data is displayed through a very basic looking GUI made with the tkinter module.
    
@usage:
    Run this script with the necessary dependencies installed and provide the text data to be analyzed. 
    The algorithm will output the sentiment polarity score for each input.
"""

"""__imports__"""
import json
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from src.src import get_sentiment

"""__constants__"""
WINDOW_SIZE: str = "600x400"
WINDOW_TITLE: str = "Sentiment Analysis Chatbot"

class SentimentChatbotGUI:
  """
  A class representing a GUI for a sentiment analysis chatbot.

  Attributes:
  - master (Tk): The root Tkinter window.
  - chat_frame (Frame): The frame containing the chat interface.
  - output_text (ScrolledText): The text widget for displaying chat messages.
  - input_entry (Entry): The entry widget for user input.
  - analyze_button (Button): The button for analyzing user input.
  - exit_button (Button): The button for exiting the application.

  Methods:
  - __init__(self, master): Initializes the SentimentChatbotGUI instance.
  - analyze_sentence(self): Analyzes the user input and displays the chatbot's response.
  """

  def __init__(self, master):
    """
    Initializes the SentimentChatbotGUI instance.

    Parameters:
    - master (Tk): The root Tkinter window.
    """
    self.master = master
    master.title(WINDOW_TITLE)
    master.geometry(WINDOW_SIZE)

    self.chat_frame = tk.Frame(master, bg="gray")
    self.chat_frame.pack(expand=True, fill="both")

    self.output_text = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, width=60, height=10)
    self.output_text.pack(side=tk.TOP, fill="both", expand=True, padx=10, pady=10)

    self.input_entry = ttk.Entry(self.chat_frame, style="Rounded.TEntry")
    self.input_entry.pack(side=tk.TOP, fill="both", expand=True, padx=10, pady=10)

    self.analyze_button = tk.Button(master, text="Analyze", command=self.analyze_sentence, bg="green", fg="black", padx=10)
    self.analyze_button.pack(side=tk.LEFT, padx=(10, 5), pady=5)

    self.exit_button = tk.Button(master, text="Exit", command=self.master.destroy, bg="green", fg="black", padx=10)
    self.exit_button.pack(side=tk.RIGHT, padx=(5, 10), pady=5)

    style = ttk.Style()
    style.configure("Rounded.TEntry", padding=(10, 5), relief="flat", background="gray", borderwidth=5, focuscolor="green", focusthickness=2)

    self.input_entry.bind("<Return>", lambda event: self.analyze_sentence())

  def analyze_sentence(self):
    """
    Analyzes the user input and displays the chatbot's response.
    """
    sentence = self.input_entry.get()
    if sentence:
      response = chatbot_response(sentence)
      self.output_text.insert(tk.END, f"You: \"{sentence}\"\nChatbot: {response}\n\n")
      self.output_text.yview(tk.END)
      self.input_entry.delete(0, tk.END)

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
  return f"\n{json_data}"

def main():
  """
  This function initializes the GUI for the Sentiment Chatbot and starts the main event loop.
  """
  root = tk.Tk()
  gui = SentimentChatbotGUI(root)
  gui.analyze_button.configure(bg="green")
  gui.exit_button.configure(bg="green")
  root.mainloop()

if __name__ == "__main__":
    main()

