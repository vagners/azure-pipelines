import json as j
import xml.etree.cElementTree as e
import sys

USAGE = f"Usage: -i <horusec-output.json> -o <junit-output.xml>"

def main() -> None:
    args = sys.argv[1:]

    if not args:
        raise SystemExit(USAGE)

    #opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    with open(args[0]) as horusecOutputFile: 
      d = j.load(horusecOutputFile)

    analysisVulnerabilities = d["analysisVulnerabilities"]
    totalTests = len(analysisVulnerabilities)

    testsuites = e.Element("testsuites")
    testsuites.set('name', 'Horusec Scan')
    testsuites.set('failures', str(totalTests))
    testsuites.set('tests', str(totalTests))

    id = 0
    for item in analysisVulnerabilities:
        testsuite = e.SubElement(testsuites,"testsuite")
        testsuite.set('failures', "1")
        testsuite.set('id', str(id))
        testsuite.set('name', item['vulnerabilities']['file'])
        testsuite.set('timestamp', item['createdAt'])
        id += 1    
        testcase = e.SubElement(testsuite,"testcase")    
        name = item['vulnerabilities']['details'].split('\n')[0]
        testcase.set('classname', item['vulnerabilities']['severity'])
        testcase.set('name', name)
    
        failure = e.SubElement(testcase,"failure") 
        failure.set('message', item['vulnerabilities']['details'])
        failure.text = 'Line: ' + item['vulnerabilities']['line'] + '\n' + 'Column: ' + item['vulnerabilities']['column'] + '\n' + 'Confidence: ' + item['vulnerabilities']['confidence'] + '\n' + 'File: ' + item['vulnerabilities']['file'] + '\n' + 'Code: ' + item['vulnerabilities']['code']

    xml = e.ElementTree(testsuites)
    xml.write(args[1])

if __name__ == "__main__":
    main()
