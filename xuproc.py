import xml.etree.ElementTree as ET
import sys
import os


def load_xml(file):
    """
    load and parse xml file
    Args:
        file (str): full or relative path to file
    returns:
        parsed xml root element
    """
    if not os.path.exists(file):
        print(f"Error: The file {file} doesn't exist. Please check path and file name")
        sys.exit(1)

    try:
        tree = ET.parse(file)
        return tree.getroot()  # root element of xml tree
    except ET.ParseError as e:
        print( f"Error: xml file {file} could not be parsed\nError: {e}")
        print(f"Hint: ensure that the file {file} is a properly formatted xml file")
        sys.exit(1)


def concat_attribs(testcase):
    """
    concatenates the classname value to the name value in the testcase element
    Args:
        testcase (Element) #XML element
    Return:
        None               #Modifies element (in memory) in place
    """

    classname = testcase.get("classname")
    name = testcase.get("name")

    if classname and name and not name.startswith(classname):
        name_update = f"{classname}.{name}"
        testcase.set("name", name_update)


def print_stats(xml_root):

    total_tests = len(xml_root.findall(".//testcase"))
    failures = len(xml_root.findall(".//testcase/failure"))
    errors = len(xml_root.findall(".//testcase/error"))
    skipped = len(xml_root.findall(".//testcase/skipped"))

    print("\n" + "Test Statistics".center(40, "=") + "\n")
    print(f"Total tests".ljust(30, ".") + f"{total_tests}".rjust(10))
    print(f"Failed".ljust(30, ".") + f"{failures}".rjust(10))
    print(f"Skipped".ljust(30, ".") + f"{skipped}".rjust(10))
    print(f"Errors".ljust(30, ".") + f"{errors}".rjust(10))
    print("\n" + "=" * 40 + "\n")


def print_help():
    text = """
    usage:
        xuproc.py [options] [xml_file]

    options:
        -h      Provides the help for using this script. (shows this help message and
                exits)
        -j      Will update each test case in the xml file as follows: 
                If there is a `classname` and `name` attribute in a `testcase` element, then
                the `name` attribute value is updated by concantenating the `classname`
                attribute value with the `name` attribute value, seperated by `.` (dot) character. 
                NOTE: Once the -j option is envoked on a file, subsequent envokations will have no
                further effect on the given file. 

    example: 
            xuproc.py -j tests.xml   # Concatenates classname and name attributes in tests.xml
            xuproc.py tests.xml      # Prints the statistics about the total number of tests, failures, errors, and skipped tests in the test file
            """
    print(text)


def main():

    if len(sys.argv) < 2 or "-h" in sys.argv:
        print_help()
        sys.exit(0)

    # check -j option 
    j_option = len(sys.argv) > 1 and sys.argv[1] == "-j"
    file_path = sys.argv[-1]

    # load xml text file
    xml_root = load_xml(file_path)

    if j_option:
        # if -j option is provided: loopthrough each testcase element and update the name attrib
        for testcase in xml_root.findall(".//testcase"):
            concat_attribs(testcase)

        # save modified name attrib to file
        tree = ET.ElementTree(xml_root)
        tree.write(file_path, encoding="UTF-8", xml_declaration=True)
        print(f"XML file updated and saved: {file_path}")
    else:
        # if the -j option is not provided: give test stats
        print_stats(xml_root)


if __name__ == "__main__":
    main()