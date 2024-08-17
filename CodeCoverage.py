import os
import xml.etree.ElementTree as ET

class CodeCoverage():
    def __init__(self, directory):
        self.directory = directory

        self.xml_file = os.path.join(self.directory, 'app', 'build', 'reports', 'jacoco', 'test', 'jacocoTestReport.xml')
        self.html_file = os.path.join(self.directory, 'app', 'build', 'reports', 'jacoco', 'test', 'html', 'index.html')

        # if not os.path.exists(self.xml_file) or not os.path.exists(self.html_file):
        #     raise FileNotFoundError("No code coverage reports found.")
    

    def get_coverage(self, name, file_path):
        element = self._get_element(name, file_path)

        if element is None: 
            return "Element not found in XML file"

        counts = self._get_count(element)
        return counts 

    def _get_element(self, name, file_path):
        tree = ET.parse(self.xml_file)
        root = tree.getroot()

        sourcefilename = file_path.split('/')[-1]

        for package in root.findall('package'):
            for class_element in package.findall('class'):
                if class_element.attrib.get('sourcefilename') == sourcefilename:
                    if class_element.attrib.get('name') == name:
                        return class_element
                    else:
                        for method in class_element.find_all('method'):
                            if method.attrib.get("name") == name:
                                return method


    def _get_count(self, element):
        counts = dict()

        for counter in element.findall('counter'):
            counts[counter.attrib['type']] = {'missed': int(counter.attrib["missed"]),
                                              'covered': int(counter.attrib["covered"])}
        
        return counts
    
    def get_percentage(self, counts):
        line_count = counts['LINE']

        missed = line_count['missed']
        covered = line_count['covered']
        
        return (covered/(missed+covered))*100

if __name__ == '__main__':
    coverage = CodeCoverage('root')
    print(coverage.get_coverage('BorrowRecord', 'root/app/src/main/java/BorrowRecord.java'))