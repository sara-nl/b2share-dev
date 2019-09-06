from argparse import ArgumentParser
from argparse import FileType
from lxml import etree
from io import StringIO
from io import BytesIO
import json
import sys
import os
import logging
import re
import requests

TOKEN = None

def load_xsd_file(filename):
    """
    load XSD file and parse it as etree.XMLSchema
    """
    with open(filename, 'rb') as fp:
        doc = etree.parse(BytesIO(fp.read()))
        return etree.XMLSchema(doc)


def load_xml_file(filename):
    """
    load XML from file
    """
    with open(filename, 'rb') as fp:
        return etree.parse(BytesIO(fp.read()))


def classify_error(msg):
    """
    parse xml schema error and classify
    """
    regex_elem_content = re.compile('^.+' +
                                    '(ERROR:SCHEMASV:[^:]+):' +
                                    ' Element \\\'{.+}(.*?)\\\': +(.*?)\\.' +
                                    '( +Expected[^(]+(\\((.*)\\))?.)?$')

    regex_parse_ns_field = re.compile('^{.+}(.*)$')

    def classify_error_details(items):
        ret = []
        for item in items:
            item = item.strip()
            m2 = regex_parse_ns_field.match(item)
            if m2 is None:
                smsg = str(msg)
                raise RuntimeError('cannot deduce error type:\n{0}'.format(smsg))
            else:
                ret.append(m2.group(1))
        ret.sort()
        return ret

    m = regex_elem_content.match(str(msg))
    if m is None:
        smsg = str(msg)
        raise RuntimeError('cannot deduce error type:\n{0}'.format(smsg))
    else:
        return {
            'errtype': m.group(1),
            'element': m.group(2),
            'msg': m.group(3).replace(',', '/')}


def validate_xml(schema, doc, community=None, name=None):
    """
    validate document against schema
    """
    ret = {
        'community': ('unknown' if community is None else community),
        'name': ('unknown' if name is None else name),
        'errtype': False,
        'element': '',
        'msg': ''
    }
    try:
        schema.assertValid(doc)
        return ret
    except etree.DocumentInvalid as err:
        log = schema.error_log
        for item in log:
            print(str(item))
        for item in log:
            err = classify_error(item)
            ret.update(err)
            return ret
    except Exception as e:
        print('Unknown error, exiting:' + str(e))
        raise


def iterate_records(baseurl):
    """
    Iterate over all records exposed by the B2SHARE server
    """
    url = "{0}/api/records/?access_token={1}".format(baseurl, TOKEN)
    while url:
        r = requests.get(url)
        data = r.json()
        # import pprint
        #pprint.pprint(data)
        for hit in data.get('hits', {}).get('hits', []):
            yield hit
        url = data.get('links', {}).get('next', None)
        if url:
            url = '{0}&access_token={1}'.format(url, TOKEN)


def get_record(baseurl, record_id):
    url = "{0}/api/records/{1}?access_token={2}".format(baseurl,
                                                        record_id,
                                                        TOKEN)
    r = requests.get(url)
    data = r.json()
    return data


def get_oai_pmh(baseurl, record_id, prefix):
    """
    retrieve OAI PMH xml
    """
    tmp_url = '{baseurl}/api/oai2d?verb=GetRecord&metadataPrefix={prefix}'
    tmp_url += '&identifier=oai:b2share.eudat.eu:b2rec/{record_id}'
    url = tmp_url.format(baseurl=baseurl,
                         prefix=prefix,
                         record_id=record_id)
    try:
        doc = etree.parse(url)
        # print(etree.tostring(doc, pretty_print=True).decode())
        return doc
    except OSError as e:
        json_record = get_record(baseurl, record_id)
        # import pprint
        # pprint.pprint(json_record, indent=4)
        # print("------------------")
        # print(url)
        # r = requests.get(url)
        # print(r.text)
        # print("++++++++++++++++++")
        # print(e)
        raise


def get_data_cite_resource(oai_xml):
    resource = oai_xml.find('.//ns:GetRecord/ns:record/ns:metadata/dc:resource',
                            {'ns': "http://www.openarchives.org/OAI/2.0/",
                             'dc': "http://datacite.org/schema/kernel-3"})
    return etree.ElementTree(resource)


def print_validation_result(resource, validation):
    print("Input:")
    print("------")
    print(etree.tostring(resource,
                         pretty_print=True).decode("utf-8"))
    print("Result:")
    print("------")
    print(validation)
    print("-------")


def main():
    language_count = {}
    descr = 'Validate Datacite / OpenAire Schemas.'
    parser = ArgumentParser(description=descr)
    parser.add_argument('--schema', type=str, help='XSD file', required=True)
    parser.add_argument('--xmlfile', type=str, help='input file')
    parser.add_argument('--baseurl', type=str, help='url',
                        default="http://127.0.0.1:5000")
    parser.add_argument('--token', type=FileType('r'))
    parser.add_argument('--prefix',
                        type=str,
                        help='MetaData prefix',
                        choices=['oai_openaire',
                                 'oai_datacite',
                                 'oai_datacite3',
                                 'oai_datacite4',
                                 'marcxml'],
                        default='oai_openaire')
    parser.add_argument('--verbose', action="store_true")
    parser.add_argument('--print_xml', action="store_true", help="print xml documents")
    parser.add_argument('--lang', help="aggregate languages", action="store_true")
    parser.add_argument('--validate', help="validate oai_pmh", action="store_true")
    args = parser.parse_args()
    TOKEN = "".join(args.token.readlines())
    schema = load_xsd_file(args.schema)
    prefix = args.prefix
    print_xml = args.print_xml
    print("i,community,name,errtype,element")
    if args.xmlfile is not None:
        doc = load_xml_file(args.xmlfile)
        result = validate_xml(schema, doc, name=args.xmlfile)
        print(json.dumps(result))
    else:
        baseurl = args.baseurl
        i = 0
        for record in iterate_records(baseurl):
            i += 1
            community = record.get('metadata', {}).get('community', '')
            language = record.get('metadata', {}).get('language', '')
            if language not in language_count:
                language_count[language] = 0
            language_count[language] += 1
            if args.validate:
                try:
                    oai_pmh = get_oai_pmh(baseurl,
                                          record['id'],
                                          prefix)
                    resource = get_data_cite_resource(oai_pmh)
                    validation = validate_xml(schema,
                                              resource,
                                              community=community,
                                              name=record['id'])
                    if print_xml:
                        print_validation_result(resource, validation)
                    if not validation['errtype']:
                        validation['errtype'] = '' 
                except Exception as e:
                    validation = {'community': community,
                                  'name': record['id'],
                                  'errtype': str(e).replace(',', ''),
                                  'element': ''}
                    print("{i},{community},{name},{errtype},{element}".
                          format(i=i, **validation))

    if args.lang:
        import pprint
        pprint.pprint(language_count, indent=4)
    print("number of records: {0}".format(i))

if __name__ == "__main__":
    main()
