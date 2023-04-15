from flask import Flask, render_template, request
import requests
import bs4
import difflib
import googlesearch
from bs4 import BeautifulSoup
from googlesearch import search
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run.py', methods=['POST'])
def search():
    input_text = request.form['input_text']

    # Search for top 5 results for input text on Google
    search_results = search(input_text, num_results=10)

    # Loop through each search result and extract content
    for result in search_results:
        try:
            # Get the HTML content of the search result
            response = requests.get(result)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the text content from the HTML
            content = soup.get_text()

            # Find similarities with input text
            similarity = difflib.SequenceMatcher(
                None, input_text.lower(), content.lower()).ratio()

            # Display the similarity and source of the content
            outputFile = open("output.txt", 'a+')
            outputFile.write((f"Similarity with {result}: {similarity}\n"))
            outputFile.close()
        except Exception as e:
            # Handle any errors that occur during the search or extraction of content
            print(f"Error in processing {result}: {e}")

        # Perform Google search and similarity check as before

        # Return a response with the similarity results
        with open('output.txt', 'r') as f:
            similarity_results = f.read()
        return similarity_results

if __name__ == '__main__':
    app.run()