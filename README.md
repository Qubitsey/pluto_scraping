# Web Scraping - Pluto.tv

**Overview**

For this project, movie and TV show data will be scraped from Pluto.tv, a well-known platform that collects material from a variety of streaming providers. The scraping is achieved using Python, leveraging the Requests library for HTTP requests and BeautifulSoup for HTML parsing. Instead of utilizing Pluto.TV APIs, we extract information directly from the HTML structure of the website.

**Project Workflow**
1. Web Scraping:
BeautifulSoup is a tool used by Python programs to parse HTML structure. Sending HTTP queries to the Pluto.tv website in order to obtain pertinent information about movies and TV shows is part of this procedure. The application gathers information by methodically browsing the HTML of the website and extracting titles, genres, durations, descriptions, etc.


2. Data Export:
Once the script is complete, the final results are saved in a CSV file with its execution time information. This format ensures the data is structured and easy to share, allowing for further analysis or visualization. The CSV file can be used by other tools and platforms to create charts, graphs, and reports, making the insights accessible and actionable for a wider audience.

3. Data Filtering and Analysis:
Numpy and Pandas is a potent Python data manipulation package that is used to process and filter data once it has been scraped. Pandas in Jupter Notebook facilitates comprehensive data exploration, enabling statistical analysis and the production of content insights, including the identification of patterns and trends.

### Prerequisites

The project requires Python 3 installed on the system.

### Installation

1. Clone the Git
```
git clone https://github.com/Qubitsey/pluto_scraping/blob/main
```

2. Enter the project folder

```
cd pluto_scraping
```

3. Create and activate the virtual environment

**Linux/MacOS**
```
python3 -m venv venv/
source venv/bin/activate
```
**Windows**
```
python3 -m venv venv/
\venv\Scripts\activate.bat
```
 4. Install dependencies

```
pip install requests pandas beautifulsoup4 concurrent.futures
```

 5. Run the script

```
python pluto_scraping.py
```
6. Check the result
The script will generate a CSV file named based on the runtime, such as pluto_227s.csv. This file will be in the same folder where you ran the script.
Additionally, the script will display the name of the generated file and the total execution time in the console. Open the generated file with any text editor, Excel, or any software that supports CSV files.
