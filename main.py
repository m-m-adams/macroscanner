from oletools.olevba import VBA_Parser, TYPE_OLE, TYPE_OpenXML, TYPE_Word2003_XML, TYPE_MHTML
import oletools
import os
import sys
import pdf_triage

input = '/home/mark/leak'
# traverse root directory, and list directories as dirs and files as files

def run_recurse(dir, condition, func):
    for root, dirs, files in os.walk(dir):
        #path = root.split(os.sep)
        #print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            #print(len(path) * '---', file)
            if condition(file):
                func(os.path.join(root, file))

def doc_cond(file):
    ext = [".doc", ".docx", '.xls', '.xlsx', '.xlsm', '.docm', '.ppt', '.pptx']
    if file.endswith(tuple(ext)):
        if not file.startswith("~$"):
            return True
    return False

def olevba_trig(file):
    try:
        vbaparser = VBA_Parser(file)
        if vbaparser.detect_vba_macros():
            for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
                print ('Filename    :', filename)
                print ('OLE stream  :', stream_path)
                print ('VBA filename:', vba_filename)
                print ('- '*39)
                print (vba_code)
                print ('- '*39)

                results = vbaparser.analyze_macros()
                for kw_type, keyword, description in results:
                    print ('type=%s - keyword=%s - description=%s' % (kw_type, keyword, description))

                print ('AutoExec keywords: %d' % vbaparser.nb_autoexec)
                print ('Suspicious keywords: %d' % vbaparser.nb_suspicious)
                print ('IOCs: %d' % vbaparser.nb_iocs)
                print ('Hex obfuscated strings: %d' % vbaparser.nb_hexstrings)
                print ('Base64 obfuscated strings: %d' % vbaparser.nb_base64strings)
                print ('Dridex obfuscated strings: %d' % vbaparser.nb_dridexstrings)
                print ('VBA obfuscated strings: %d' % vbaparser.nb_vbastrings)
                print ("\n")

    except:
        e = sys.exc_info()[0]
        print (f'{e} from {file}')

run_recurse(input, pdf_triage.pdf_cond, pdf_triage.triagePDF)