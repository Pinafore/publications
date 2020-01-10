from typing import Text
<<<<<<< HEAD
import subprocess
import tempfile
import argparse
=======
import glob
import subprocess
import tempfile
import argparse
import re
>>>>>>> 8d95281fddc4325378a9dcdc7d2cdac6cfcf95b2



SPELL_FILE = '/tmp/spellcheck_tmp.tex'


def write_disk(text: Text):
    with open(SPELL_FILE, 'w') as f:
        f.write(text)


def hunspell_text(text: Text):
    write_disk(text)
<<<<<<< HEAD
    cmd = subprocess.run(f'hunspell -d en_US -a -t {SPELL_FILE}', shell=True, capture_output=True)
=======
    cmd = subprocess.run(f'hunspell -p scripts/hunspell_dictionary.dic -d en_US -a -t {SPELL_FILE}', shell=True, capture_output=True)
>>>>>>> 8d95281fddc4325378a9dcdc7d2cdac6cfcf95b2
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
<<<<<<< HEAD
        for idx, line in enumerate(f, start=1):
=======
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

>>>>>>> 8d95281fddc4325378a9dcdc7d2cdac6cfcf95b2
            text = line.strip()
            out = hunspell_text(text)
            errors = []
            for entry in out:
                if entry != '' and entry != '*':
                    errors.append(entry)

            if len(errors) > 0:
                for e in errors:
                    word, offset, suggests = parse_error(e)
<<<<<<< HEAD
=======
                    # Probably not a typo, just something with a number
                    if re.search('[0-9]', word):
                        continue

>>>>>>> 8d95281fddc4325378a9dcdc7d2cdac6cfcf95b2
                    if len(suggests) > 0:
                        suggested_line = f' - {suggests}'
                    else:
                        suggested_line = ''
                    print(f'{filename}:{idx}:{offset}: (Typo) {word}{suggested_line}')
<<<<<<< HEAD
                print()
=======
>>>>>>> 8d95281fddc4325378a9dcdc7d2cdac6cfcf95b2


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--files', nargs='+')
    args = parser.parse_args()

    for filename in args.files:
<<<<<<< HEAD
        check_file(filename)
=======
        if '*' in filename:
            for expanded_filename in glob.glob(filename):
                check_file(expanded_filename)
        else:
            check_file(filename)
>>>>>>> 8d95281fddc4325378a9dcdc7d2cdac6cfcf95b2


if __name__ == '__main__':
    main()