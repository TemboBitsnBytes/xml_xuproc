import pytest
import xml.etree.ElementTree as ET
from io import StringIO
import os
import sys

# Import functions from xuproc
from xuproc import load_xml, concat_attribs, print_stats

# Helper function to create an XML file
@pytest.fixture
def sample_xml(tmp_path):
    xml_content = """<?xml version="1.0"?>
    <testsuites>
        <testsuite>
            <testcase classname="ClassA" name="test1"/>
            <testcase classname="ClassB" name="test2">
                <failure message="failed assertion"/>
            </testcase>
            <testcase classname="ClassC" name="test3">
                <error message="error occurred"/>
            </testcase>
            <testcase classname="ClassD" name="test4"/>
        </testsuite>
    </testsuites>"""
    xml_file = tmp_path / "sample.xml"
    with open(xml_file, "w") as f:
        f.write(xml_content)
    return str(xml_file)

# Test load_xml function
def test_load_xml(sample_xml):
    xml_root = load_xml(sample_xml)
    assert xml_root.tag == "testsuites"
    assert len(xml_root.findall(".//testcase")) == 4

def test_load_xml_file_not_found():
    with pytest.raises(SystemExit):
        load_xml("non_existent_file.xml")

def test_concat_attribs(sample_xml):
    xml_root = load_xml(sample_xml)
    testcase = xml_root.find(".//testcase[@classname='ClassA']")
    concat_attribs(testcase)
    assert testcase.get("name") == "ClassA.test1"

def test_concat_attribs_no_update(sample_xml):
    xml_root = load_xml(sample_xml)
    testcase = xml_root.find(".//testcase[@classname='ClassB']")
    concat_attribs(testcase)
    assert testcase.get("name") == "ClassB.test2"  # Already correct

def test_print_stats(capsys, sample_xml):
    xml_root = load_xml(sample_xml)
    print_stats(xml_root)
    captured = capsys.readouterr()
    assert "Total tests" in captured.out
    assert "4" in captured.out  # Total test cases
    assert "1" in captured.out  # 1 failure
    assert "1" in captured.out  # 1 error
    assert "0" in captured.out  # No skipped tests

