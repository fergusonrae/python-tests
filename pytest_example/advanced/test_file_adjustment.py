""" Tests for file_adjustments.py"""

from pathlib import Path
from unittest.mock import patch
import uuid

from lxml import etree
import pytest

import file_adjustments as fa

########################
### helper functions ###
########################

def get_xml_tree(a_value: str) -> etree:
    root = etree.Element('root')
    if a_value:
        etree.SubElement(root, 'A').text = a_value
    etree.SubElement(root, 'B').text = 'not specified'
    tree = etree.ElementTree(root)
    return tree

def create_xml_file(directory: Path, a_value: str) -> Path:
    xml_file = directory / (str(uuid.uuid4()) + '.xml')
    tree = get_xml_tree(a_value)
    tree.write(str(xml_file), xml_declaration=True, encoding='utf-8')
    assert xml_file.is_file()
    return xml_file

##################
### file tests ###
##################

# This test takes the global temp_dir fixture found in conftest.py
# Here, we focus on testing what this particular function asserts
# not what the other functions is calls create
@patch.object(fa, "update_xml_a_value")
def test_update_xml_directory(mock_a, temp_dir):
    """Tests for update_xml_a_value(tree_xml: etree, val: str) -> None"""

    val = 'foo'
    xml_directory = temp_dir / 'temp_xml_directory'

    # Assert throws an error if the directory passed does not exist
    with pytest.raises(FileNotFoundError):
        fa.update_xml_directory(xml_directory, val)
    
    # If directory exists but contains no files, no error
    xml_directory.mkdir()
    fa.update_xml_directory(xml_directory, val)

    # If directory exists with two xml files and one non-xml, changes the xml but does not affect non-xml
    # This can be seen by it calling the function update_xml_a_value twice
    xml_file_1 = create_xml_file(xml_directory, 'hey')
    xml_file_2 = create_xml_file(xml_directory, 'ho')
    xml_file_3 = create_xml_file(xml_directory, 'bar')
    xml_change_suffix = xml_file_3.with_suffix('.zzz')
    xml_file_3.rename(xml_change_suffix)
    fa.update_xml_directory(xml_directory, val)
    assert mock_a.call_count == 2
    for xml_file in [xml_file_1, xml_file_2, xml_change_suffix]:
        assert xml_file.is_file()
    assert len([f for f in xml_directory.iterdir()]) == 3

def test_update_xml_a_value():
    """Tests for update_xml_a_value(tree_xml: etree, val: str) -> None"""

    # When A attribute does not exist, throw AttributeError
    test_tree = get_xml_tree(None)
    with pytest.raises(AttributeError):
        fa.update_xml_a_value(test_tree, 'set')

    # When A attribute exists, overwrite
    test_tree = get_xml_tree('not_set')
    fa.update_xml_a_value(test_tree, 'set')
    root = test_tree.getroot()
    assert root.find('A').text == 'set'
    assert root.find('B').text != 'set'