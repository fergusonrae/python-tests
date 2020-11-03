"""Functions to manipulate location and value of files"""

from pathlib import Path
import shutil

from lxml import etree

def update_xml_directory(directory: Path, a_val: str) -> None:
    """Resets desired values of all xml files in the directory passed in"""
    for xml_file in [f for f in directory.iterdir() if f.suffix == '.xml']:
        tree_xml = etree.parse(str(xml_file))
        update_xml_a_value(tree_xml, a_val)
        tree_xml.write(str(xml_file))

def update_xml_a_value(tree_xml: etree, val: str) -> None:
    """Overwrites the 'A' value of the xml value"""
    root = tree_xml.getroot()
    root.find('A').text = val