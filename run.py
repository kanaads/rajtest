from flask import Flask, render_template, request
import requests
import bs4
import difflib
import googlesearch as gs
from bs4 import BeautifulSoup
from googlesearch import search
import requests
import math

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    input_text = request.form['input_text']
    # Search for top 5 results for input text on Google
    search_results = gs.search(input_text, num_results=5)

    # Create an empty list to store the similarity results
    similarity_results = []
    dict_res={}

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

            # Add the similarity and source of the content to the list
            similarity_results.append({'url': result, 'similarity': similarity})
            dict_res[result]=math.ceil(similarity*100)
            
        except Exception as e:
            # Handle any errors that occur during the search or extraction of content
            print(f"Error in processing {result}: {e}")
        

    # Render a template to display the similarity results
    return render_template('results.html', similarity_results=similarity_results)


if __name__ == '__main__':
    app.run(debug=True)