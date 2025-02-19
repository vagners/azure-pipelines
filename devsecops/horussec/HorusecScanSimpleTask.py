import json as j
import xml.etree.cElementTree as e
import sys
import os
import os.path

USAGE = f"Usage: -p <source directory> -o <junit-output-file.xml>"


def convert_horusec_output(input_file, output_file, total_scannned_files) -> None:
    with open(input_file) as horusecOutputFile:
        d = j.load(horusecOutputFile)

    # Se não houver vulnerabilidades, defina como lista vazia
    analysisVulnerabilities = d.get("analysisVulnerabilities") or []
    totalTests = len(analysisVulnerabilities)

    testsuites = e.Element("testsuites")
    testsuites.set('name', 'Horusec Scan')
    testsuites.set('failures', str(totalTests))
    testsuites.set('tests', str(total_scannned_files))

    print('totalTests: ' + str(totalTests))
    print('total_scannned_files: ' + str(total_scannned_files))

    id = 0
    for item in analysisVulnerabilities:
        testsuite = e.SubElement(testsuites, "testsuite")
        testsuite.set('id', str(id))
        testsuite.set('name', item['vulnerabilities']['file'])
        testsuite.set('timestamp', item['createdAt'])
        id += 1
        testcase = e.SubElement(testsuite, "testcase")
        name = item['vulnerabilities']['details'].split('\n')[0]
        testcase.set('classname', item['vulnerabilities']['severity'])
        testcase.set('name', name)

        failure = e.SubElement(testcase, "failure")
        failure.set('message', item['vulnerabilities']['details'])
        failure.text = (
            'Line: ' + item['vulnerabilities']['line'] + '\n'
            + 'Column: ' + item['vulnerabilities']['column'] + '\n'
            + 'Confidence: ' + item['vulnerabilities']['confidence'] + '\n'
            + 'File: ' + item['vulnerabilities']['file'] + '\n'
            + 'Code: ' + item['vulnerabilities']['code']
        )

    xml = e.ElementTree(testsuites)
    xml.write(output_file)

def scan_directory(source_directory, horusec_output_file) -> int:
    command = 'curl -fsSL https://raw.githubusercontent.com/ZupIT/horusec/main/deployments/scripts/install.sh | bash -s latest'
    print(command)
    os.system(command)

    command = 'horusec start -D -i ' + \
        sys.argv[0]+' -p "'+source_directory + \
        '" -o="json" -O="'+horusec_output_file+'"'
    print(command)
    os.system(command)

    total_scannned_files = sum([len(files)
                               for r, d, files in os.walk(source_directory)])

    return total_scannned_files


def main() -> None:
    args = sys.argv[1:]

    if not args:
        raise SystemExit(USAGE)

    #opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]

    source_directory = args[0]
    output_file = args[1]
    horusec_output_file = './output.json'

    total_scannned_files = scan_directory(
        source_directory, horusec_output_file)

    convert_horusec_output(horusec_output_file,
                           output_file, total_scannned_files)


if __name__ == "__main__":
    main()
