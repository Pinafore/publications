import os
import sys
import re

# 0. Remove the keywords with brace.
# 1. Remove the keywords when keeping the contents.
# 2. Remove the caption_keywords in begin ... end with caption keeping.
# 3. Remove the scope_keywords in begin ... end.
# 4. Remove the equation pairs.
# 5. Remove the backslash.
remove_keywords = ['cite', 'ref', 'item']
keywords = ['section', 'subsection', 'subsubsection', 'subsubsubsection', 'chapter', 'textbf', 'emph']
caption_keywords = ['figure', 'table', 'longtable']
scope_keywords = ['equation', 'eqnarray']
pairs = ['$']

def latex2txt(in_str):
    p = re.compile(r'^%.*?$', re.S | re.M)
    out_str = p.sub('', in_str)
    for keyword in remove_keywords:
        p = re.compile(r'\\%s\{(.+?)\}' % keyword)
        out_str = p.sub('', out_str)
        p = re.compile(r'\\%s' % keyword)
        out_str = p.sub('', out_str)

    for keyword in keywords:
        p = re.compile(r'\\%s\{(.+?)\}' % keyword)
        out_str = p.sub(r'\1', out_str)

    for keyword in caption_keywords:
        p = re.compile(r'\\begin\{%s\}.*?\\caption\{(.+?)\}.*?\\end\{%s\}' % (keyword, keyword),
                re.S)
        out_str = p.sub(r'\1\n', out_str)

    for keyword in scope_keywords:
        p = re.compile(r'\\begin\{%s\}.*?\\end\{%s\}' % (keyword, keyword),
                re.S)
        out_str = p.sub('', out_str)

    for pair in pairs:
        re_pair = re.escape(pair)
        p = re.compile(r'%s.*?%s' % (re_pair, re_pair), re.S)
        out_str = p.sub('', out_str)

    p = re.compile(r'\\\S*?\{.+?\}\[.+?\]')
    out_str = p.sub('', out_str)
    p = re.compile(r'\\\S*?\{.+?\}')
    out_str = p.sub('', out_str)
    p = re.compile(r'\\')
    out_str = p.sub('', out_str)

    return out_str


def print_usage():
    print('Usage: latex2txt.py output_file input_file1 [input_file2 ...]')
    exit(-1)


def main():
    if len(sys.argv) < 3:
        print_usage()

    output_name = sys.argv[1]
    input_names = sys.argv[2:]
    with open(output_name, 'w') as out_file:
        for input_name in input_names:
            with open(input_name) as in_file:
                input_content = in_file.read()
            output_content = latex2txt(input_content)
            out_file.write(output_content + '\n')


if __name__ == '__main__':
    main()
