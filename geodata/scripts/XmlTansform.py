import lxml
import xml.etree as ET
import xml.dom as DOM
from lxml import etree
import lxml
from lxml import etree
from bs4 import BeautifulSoup
import csv


class XmlTransformer:
    def __init__(self):
        self.xml_parser = etree.XMLParser(recover=True)

    def transform_xml(self, xml_string, xslt_string):
        try:
            xml_doc = lxml.etree.fromstring(xml_string)
        except lxml.etree.XMLSyntaxError as e:
            print(f"XML parsing error. Details: {e}")
            return None
        xslt_doc = lxml.etree.fromstring(xslt_string)
        transform = etree.XSLT(xslt_doc)
        result = transform(xml_doc)
        return str(result)

    def xml_file_to_kml_file(self, file):
        with open(file, 'r') as f:
            xml_string = f.read()
        xslt_string = """
        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <kml xmlns="http://www.opengis.net/kml/2.2">
                    <Document>
                    </Document>
                </kml>
            </xsl:template>
            <xsl:template match="Placemark">
                <Placemark>
                    <name><xsl:value-of select="name"/></name>
                    <description><xsl:value-of select="description"/></description>
                    <Point>
                        <coordinates><xsl:value-of select="coordinates"/></coordinates>
                    </Point>
                </Placemark>
            </xsl:template>
        </xsl:stylesheet>
        """
        return self.transform_xml(xml_string, xslt_string)

    def extract_coordinates(self, file)->None:
        # TODO FINISH
        latitude = ""
        longitutde = ""
        corrected = f"""
        var map = new Microsoft.Maps.Map(document.getElementById('mapDiv'), {{
            credentials: 'Your Bing Maps Key'}});
            var latlong = new Microsoft.Maps.Location(latitude, longitude);
            var pin = new Microsoft.Maps.Pushpin(latlong);
            map.entities.push(pin);
        """
        with open(file, 'r') as f:
            xml_string = f.readlines()
            soup = BeautifulSoup(xml_string, 'xml')
            coordinates = soup.find_all('point')
            print(coordinates)


