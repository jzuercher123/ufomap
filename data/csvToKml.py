import xml.dom.minidom
import csv
import sys
import xml.etree.ElementTree as ET
from xml.dom import minidom
import logging


def write_xml(csv_file):
    # Create XML DOM object
    print("starting")
    dom_implement = xml.dom.minidom.getDOMImplementation()
    doc = dom_implement.createDocument('', "csv_as_xml", None)
    top_element = doc.documentElement

    # Read CSV file
    print("opening csv file")
    with open(csv_file, 'r') as f:
        csv_data = csv.reader(f)
        headers = next(csv_data)  # get headers from first row

        print("converting rows to xml")
        for row in csv_data:
            child = doc.createElement(headers[0])
            top_element.appendChild(child)
            for i, cell in enumerate(row):
                if i < len(headers):  # Checks if i is within the bounds of headers
                    child.setAttribute(headers[i], cell)
                i+= 1
    print("Saving XML file")
    output_file_path = "./csv_as_xml.xml"
    with open(output_file_path, "w") as f:
        f.write(top_element.toprettyxml())
        print("done")

def xml_to_kml(xml_file):
    # Load and parse the XML file into memory
    xml_tree = ET.parse(xml_file)
    xml_root = xml_tree.getroot()

    # Create new XML tree for KML
    kml_root = ET.Element('kml')
    document = ET.SubElement(kml_root, 'Document')

    for element in xml_root:
        placemark = ET.SubElement(document, 'Placemark')

        # Copy relevant elements from XML to KML
        # Note: Adjust field names as per your XML file's structure.
        name = ET.SubElement(placemark, 'name')
        name.text = element.find('shape').text  # replace with your field name

        point = ET.SubElement(placemark, 'Point')
        coordinates = ET.SubElement(point, 'coordinates')
        coordinates.text = f"{element.find('longitude_field').text},{element.find('latitude_field').text},0"  # replace with your field names

    # Use minidom to prettify the output XML
    xmlstr = minidom.parseString(ET.tostring(kml_root)).toprettyxml(indent='   ')

    # Save to KML file
    with open('output.kml', 'w') as f:
        f.write(xmlstr)


def csv_to_xml_custom(csv_file):
    dom_implement = xml.dom.minidom.getDOMImplementation()
    doc = dom_implement.createDocument(None, "records", None)
    top_element = doc.documentElement

    with open(csv_file, 'r') as f:
        csv_data = csv.reader(f)
        headers = next(csv_data)  # get headers from first row

        for row in csv_data:
            record = doc.createElement('record')
            top_element.appendChild(record)

            for i, cell in enumerate(row):
                if i >= len(headers):
                    break
                child = doc.createElement(headers[i])
                child.appendChild(doc.createTextNode(cell))
                record.appendChild(child)

    output_file_path = csv_file.split('.')[0] + "_customized.xml"
    with open(output_file_path, 'w') as f:
        f.write(top_element.toprettyxml())
    print("XML file has been created: ", output_file_path)


csv_to_xml_custom('complete.csv')

