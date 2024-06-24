import csv
from bs4 import BeautifulSoup
import requests
import re


class CsvTransform:
    def __init__(self):
        # initiate soup object with lxml parser
        self.soup = None

    def load_xml(self, url):
        """
        This function loads xml from given url and updates soup object
        :param url: URL of xml file
        """
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content, 'lxml-xml')

    def parse_xml(self):
        """
        This function parses xml and prints it
        """
        if self.soup:
            print(self.soup.prettify())

    def csv_to_geoformat(self, file):
        rows = []
        with open(file, 'r') as f:
            csv_data = csv.reader(f)
            for line in csv_data:
                new_data = []
                if len(line) > 10:  # make sure line has enough data
                    print(f"""
                    1: {line[1]}
                    2: {line[2]}
                    3: {line[3]}
                    7: {line[7]}
                    9: {line[9]}
                    10:{line[10]}
                    """)
                    new_data.append(line[1])
                    new_data.append(line[2])
                    new_data.append(line[3])
                    new_data.append(line[7])
                    new_data.append(line[9])
                    new_data.append(line[10])
                    rows.append(new_data)
                else:
                    print(f"Line has fewer columns than expected: {line}")


        with open('newfile1.csv', 'w', newline='') as f:
            headers = ["city", "state", "country", "comment", "latitude", "longitude"]
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows([row for row in rows])


    def remove_duplicate_commas(self, file):
        """
        This method removes duplicate commas from a CSV file
        :param file: The path of the CSV file
        """
        with open(file, 'r') as f:
            lines = f.readlines()

        with open(file, 'w', newline='') as f:
            for line in lines:
                line = re.sub(r',,+', ',', line)
                f.write(line)

    def csv_to_kmlschema(self, file):
        with open(file, 'r') as f:
            csv_data = csv.reader(f)
            headers = next(csv_data)
            rows = [dict(zip(headers, row)) for row in csv_data]

        kml_data = []
        for row in rows:
            if 'longitude' in row and 'latitude' in row:
                kml_data.append(
                    f"<Placemark>\n\t<region>{row['city']}</region>\n\t\t<description>{row['comment']}</description>\n\t<Point><coordinates>{row['longitude']},{row['latitude']}</coordinates>\n\t</Point>\n</Placemark>")
            else:
                print(
                    f"Warning: 'longitude' or 'latitude' is missing for city {row.get('city', '')}. This data was skipped.")

        kml = f"""
        <?xml version="1.0" standalone="yes" encoding="UTF-8"?>
        <kml xmlns="http://www.opengis.net/kml/2.2" xmlns:atom="http://www.w3.org/2000/xmlns/">
        <Document>
            {''.join(kml_data)}
        </Document>
        </kml>
        """

        with open('output.kml', 'w') as f:
            f.write(kml)


transformer = CsvTransform()
transformer.csv_to_kmlschema('newfile1.csv')