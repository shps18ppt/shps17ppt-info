import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import os
import time

def translate_to_japanese(text):
    translator = Translator()
    translation = translator.translate(text, src='en', dest='ja')
    return translation.text

url = 'https://www.worlddata.info/asia/japan/earthquakes.php'
output_file = 'latest_magnitude_info.txt'

while True:
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first <li> element with the data-date attribute
        first_earthquake = soup.find('li', {'data-date': True})

        if first_earthquake:
            magnitude_info = first_earthquake.find(class_='qtx').text.strip()

            # Translate message to Japanese
            magnitude_info_japanese = translate_to_japanese(magnitude_info)

            # Check if the information has changed
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as file:
                    old_magnitude_info = file.read()

                if magnitude_info_japanese != old_magnitude_info:
                    # Update the file with the new information
                    with open(output_file, 'w', encoding='utf-8') as file:
                        file.write(magnitude_info_japanese)
                    print("Updated magnitude information.")

            else:
                # File doesn't exist, create and write the information
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(magnitude_info_japanese)
                print("Initial magnitude information written to file.")

        else:
            print("No earthquake information found.")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

    # Sleep for 60 seconds before the next iteration
    time.sleep(60)
