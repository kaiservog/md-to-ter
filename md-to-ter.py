import sys
import re

COLOR_H1 = '\033[38;5;117m'
COLOR_H2 = '\033[38;5;39m'
COLOR_H3 = '\033[38;5;26m'
COLOR = '\033[38;5;209m'
COLOR_ORANGE = '\033[38;5;34m'

ENDC = '\033[0m'
T_BOLD = '\033[1m'
T_ITALIC = '\033[3m'
T_UNDERLINE = '\033[4m'


H6 = '######'
H5 = '#####'
H4 = '####'
H3 = '###'
H2 = '##'
H1 = '#'
CODE = '```'
HR = '***'
LIST = re.compile(r'\*\s')
COTE = '> '
#specials
NUMBER_LIST = re.compile(r'\d\.\s')
BOLD = re.compile(r'\*\*(.*?)\*\*')
ITALIC = re.compile(r'_(.*?)_')
MINI_CODE=re.compile(r'`(.*?)`')


def convert(line):
    if H6 in line:
        return T_BOLD + COLOR_H3 + line[6:] + ENDC + '\n'
    elif H5 in line:
        return T_BOLD + COLOR_H3 + line[5:] + ENDC + '\n'
    elif H4 in line:
        return T_BOLD + COLOR_H3 + line[4:] + ENDC + '\n'
    elif H3 in line:
        return T_BOLD + COLOR_H3 + line[3:] + ENDC + '\n'
    elif H2 in line:
        return T_BOLD + COLOR_H2 + line[2:] + ENDC + '\n'
    elif H1 in line:
        return T_BOLD + COLOR_H1 + line[1:] + ENDC + '\n'
    elif HR in line:
        return T_BOLD + '_________________________________' + ENDC
    elif 'y'+CODE in line:
        return T_BOLD + COLOR_ORANGE + ' [ '
    elif 'x'+CODE in line:
        return ' ]' + ENDC

    if re.search(ITALIC, line):
        while True:
            ms = re.search(ITALIC, line)
            if ms is None or len(ms.groups()) < 1:
                break
            
            line = line.replace(ms.group(0), T_ITALIC + ms.group(1) + ENDC)
            
    if re.search(MINI_CODE, line):
        while True:
            ms = re.search(MINI_CODE, line)
            if ms is None or len(ms.groups()) < 1:
                break
            
            line = line.replace(ms.group(0), T_BOLD+ COLOR_ORANGE + '[ ' +ms.group(1) + ' ]' +ENDC)
            
    if LIST.match(line):
        line = COLOR +'  * ' + ENDC + line[1:]
    if COTE in line:
        line = '  ' + COLOR + line + ENDC
    if NUMBER_LIST.match(line):
        line = '  ' + line
    if re.search(BOLD, line):
        while True:
            ms = re.search(BOLD, line)
            if ms is None or len(ms.groups()) < 1:
                break
            line = line.replace(ms.group(0), T_BOLD + ms.group(1) + ENDC)

    return line

def is_mc(line, is_mc):
    if CODE in line:
        if is_mc:
            return False
        else:            
            return True
    else:
        return is_mc
    
        
def is_multi_code(line, already_in_mc):
    if CODE in line:
        if already_in_mc:
            return " ]" + ENDC
        else:            
            return T_BOLD +"[ "
    else:
        return line
        
def toList(str):
    lines = content.split('\n')
    multiline_code = False
    
    for line in lines:
        if "```" in line:
            if multiline_code:
                multiline_code = False
                yield {'content': 'x'+line, 'proccess' : True}
            else:
                multiline_code = True
                yield {'content': 'y'+line, 'proccess' : True}
        else:
            yield {'content': line, 'proccess' : not multiline_code}

def read_file(path):
    return open(path, 'r').read()

if __name__ == '__main__':
    
    content = read_file(sys.argv[1])
       
    final = ""
    content_list = toList(content)

    for line in content_list:
        if line['proccess']:
            final += convert(line['content']) + '\n'
        else:
            final += '   ' + line['content'] + '\n'

    print(final)
    
    
    