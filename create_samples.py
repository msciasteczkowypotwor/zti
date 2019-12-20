import re


def create_header(prefixes):
    header = ""
    for p in prefixes:
        header += p
        header += NEW_LINE
    header += NEW_LINE
    return header


def create_full_inputs(header, inputs):
    full_inputs = []
    for i in inputs:
        full_input = header
        full_input += i
        full_inputs.append(full_input)
    return full_inputs


def find(text, regex):
    return re.findall(regex, text, re.M)[0]


NEW_LINE = '\n'
FINDING_INPUTS_REGEX = "<[^<]*\"\^\^xsd:string \."
FINDING_PREFIX_REGEX = "@.*"

f = open("dataset/test.xml.ttl", "r")
dataset = f.read()

full_inputs = create_full_inputs(
    create_header(
        re.findall(FINDING_PREFIX_REGEX, dataset)),
    re.findall(FINDING_INPUTS_REGEX, dataset))

counter = 1
for i in full_inputs:
    file_name = "inputs/%s.xml.ttl" % counter
    f = open(file_name, "w")
    f.write(i)

    counter = counter + 1


FINDING_REF_CONTEXT = "^<.*>$"
FINDING_PART_REF_CONTEXT = ".*char="
full_context = find("i", FINDING_REF_CONTEXT)
part_context = find(full_context, FINDING_PART_REF_CONTEXT)