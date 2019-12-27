from typing import Text
import glob
import subprocess
import tempfile
import argparse
import re



SPELL_FILE = '/tmp/spellcheck_tmp.tex'


def write_disk(text: Text):
    with open(SPELL_FILE, 'w') as f:
        f.write(text)


def hunspell_text(text: Text):
    write_disk(text)
    cmd = subprocess.run(f'hunspell -p scripts/hunspell_dictionary.dic -d en_US -a -t {SPELL_FILE}', shell=True, capture_output=True)
    return cmd.stdout.decode('utf8').strip().split('\n')[1:]


def parse_error(hun_out: Text):
    if hun_out[0] == '&':
        meta, suggests = hun_out.split(':')
        _, word, _, offset = meta.split()
        offset = int(offset)
        suggests = suggests.strip()
    elif hun_out[0] == '#':
        _, word, offset = hun_out.split()
        suggests = ''
    else:
        raise ValueError(f'Unhandled: {hun_out}')
    return word, offset, suggests


def check_file(filename):
    with open(filename) as f:
        spell_disabled = False
        for idx, line in enumerate(f, start=1):
            if 'spell-disable' in line:
                spell_disabled = True
            if 'spell-enable' in line:
                spell_disabled = False
            
            if 'spell-line-disable' in line:
                continue
            
            if spell_disabled:
                continue

            text = line.strip()
            out = hunspell_text(text)
            errors = []
            for entry in out:
                if entry != '' and entry != '*':
                    errors.append(entry)

            if len(errors) > 0:
                for e in errors:
                    word, offset, suggests = parse_error(e)
                    # Probably not a typo, just something with a number
                    if re.search('[0-9]', word):
                        continue

                    if len(suggests) > 0:
                        suggested_line = f' - {suggests}'
                    else:
                        suggested_line = ''
                    print(f'{filename}:{idx}:{offset}: (Typo) {word}{suggested_line}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+')
    args = parser.parse_args()

    for filename in args.files:
        if '*' in filename:
            for expanded_filename in glob.glob(filename):
                check_file(expanded_filename)
        else:
            check_file(filename)


if __name__ == '__main__':
    main()