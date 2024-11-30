# Defining a Recursive Function for Web Scraping all the embedded Website Text and Text from Embedded PDF Files.


# Importing Required Libraries
import requests
from bs4 import BeautifulSoup
import PyPDF2

# Declaring visited_link and pdf links as global variables so that all functions can access it
# pdf_links, visited_links, success_links = [],[],[]

# Extracting text from pdf
def extract_text_from_pdf(url):

    # Making Global Variables so that we can use throughout the function
    global pdf_links, visited_links, success_links

    try:
        if url not in visited_links:
            response = requests.get(url, stream=True)

            # Check if the content-type is a PDF
            if 'application/pdf' in response.headers['content-type']:
                with open("temp_pdf.pdf", 'wb') as temp_pdf:
                    temp_pdf.write(response.content)

                text = ""

                with open("temp_pdf.pdf", 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfFileReader(pdf_file)

                    for page_num in range(pdf_reader.numPages):
                        page = pdf_reader.getPage(page_num)
                        text += page.extractText()

                save_to_file(text)
                visited_links.append(url)
                pdf_links.append(url)

    except:
        visited_links.append(url)

def save_to_file(text):
    with open('Complete_website_data-1.txt', 'a', encoding = 'utf-8') as f:
        f.write(text)

def web_scraping_text(url):

    global pdf_links, visited_links, success_links

    if url not in visited_links and 'csvtu.ac.in' in url:
        try:
            # Requesting website access for the main website
            r = requests.get(url)

            # Create a BeautifulSoup object and parse the HTML content
            soup = BeautifulSoup(r.content, 'lxml')

            # Extract all the text from the webpage
            text = soup.get_text()

            if text is not None and text != '':
              save_to_file(text)
              success_links.append(url)

            # Find all the links on the webpage
            links = soup.find_all('a')

            visited_links.append(url)

            for link in links:
                # Creating an object and storing links
                href = link.get('href')

                # To ensure we are scraping the link which contains data from csvtu only
                if href is not None and 'csvtu.ac.in' in href and href not in visited_links:
                  # Check if the link points to a PDF
                    if href.lower().endswith('.pdf'):
                        extract_text_from_pdf(href)
                    else:
                        web_scraping_text(href)

        except requests.exceptions.ConnectTimeout as e:
            # Appending link to visited_links as we have already visited it
            visited_links.append(url)
            print(f"Connection to {url} timed out. Check your internet connection.")

        except requests.exceptions.RequestException as e:
            visited_links.append(url)
            print(f"An error occurred: {e}")

# Calling function
web_scraping_text("https://csvtu.ac.in/ew/")