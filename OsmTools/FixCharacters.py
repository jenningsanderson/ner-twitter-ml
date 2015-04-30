import sys
import getopt
import unicodedata
import os.path

from sets import Set

CHARACTER_REPLACEMENTS = {
    "128" : "",
    "130" : "", #Can't tell
    "131" : "", #Can't tell
    "132" : "", #Can't tell
    "133" : "", #Can't tell
    "134" : "",
    "136" : "", #Can't tell
    "135" : "", #Can't tell
    "137" : "", #Can't tell
    "138" : "", #Can't tell
    "139" : "", #Can't tell
    "140" : "", #Can't tell
    "141" : "", #Can't tell
    "141 139" : "", #Non-English
    "141 155" : "", #Non-English, need to look into
    "142" : "", #Can't tell
    "143" : "", #Can't tell
    "144" : "", #Can't tell
    "145" : "", #Can't tell
    "146" : "\'", #Weird
    "147" : "", #Can't tell
    "148" : "", #Can't tell
    "149" : "", #Can't tell
    "150" : "", #Can't tell
    "151" : "", #Can't tell
    "152" : "",
    "153" : "",
    "154" : "", #Can't tell
    "156" : "", #Can't tell
    "157" : "",
    "159" : "", #Can't tell
    "161" : "", #Can't tell
    "163" : "$", #Can't tell
    "165" : "", #Can't tell
    "167" : "", #Can't tell
    "169" : "", #Can't tell
    "171" : "", #Can't tell
    "172" : "",
    "180" : "$",
    "186" : "", #Maybe degree, not sure
    "187" : "", #Can't tell
    "188" : "", #Can't tell
    "190" : "", #Can't tell
    "191" : "", #Can't tell
    "192" : "", #Can't tell
    "193" : "", #Can't tell
    "194" : "", #Can't tell
    "199" : "",
    "200" : "", #Can't tell
    "201" : "", #Can't tell
    "202" : "", #Can't tell
    "208" : "", #Can't tell
    "209" : "", #Can't tell
    "210" : "", #Can't tell
    "211" : "", #Can't tell
    "212" : "", #Can't tell
    "213" : "", #Can't tell
    "219" : "", #Can't tell, $ maybe?
    "221" : "", #Can't tell
    "225" : "",
    "226" : "", #Can't tell
    "227" : "",
    "231" : "",
    "235" : "",
    "238" : "",
    "242" : "",
    "246" : "",
    "248" : "",
    "252" : "",
    "194 129" : "", #not sure, look into
    "194 141" : "", #non english character, couldn't identify
    "194 157" : "", #''
    "194 160" : "", #Nothing?
    "194 162" : "C", #Cent sign
    "194 163" : "E", #Euro symbol
    "194 166" : "|", #Weird bar
    "194 167" : "", #Weird spinning thing
    "194 168" : "", #Weird double dot
    "194 170" : "a", #Tiny a
    "194 171" : "<<", #Tiny double <<
    "194 172" : "<", #Weird down left corner
    "194 173" : "", #Can't tell
    "194 174" : "C", #C with circle
    "194 175" : "-", #High line
    "194 176" : "o", #Degree marker
    "194 177" : "+-", #+ on top of - 
    "194 178" : "^2", #2nd power symbol
    "194 182" : "P", #new paragraph sign
    "194 184" : "", #hard to tell
    "194 187" : ">>", #Tiny double >>
    "195 129" : "A", #A with accent
    "195 130" : "A", #A with carrot
    "195 131" : "A", #A with line
    "195 132" : "AE", #A with umlaut
    "195 133" : "AE", #A with umlaut
    "195 137" : "E", #E with accent
    "195 152" : "O", #O with slash
    "195 159" : "B", #Esset
    "195 161" : "a", #a with accent
    "195 162" : "a", #a with carrot
    "195 163" : "a", #a with line
    "195 164" : "ae", #a with umlaut 
    "195 165" : "a", #a wtih tiny line
    "195 166" : "[", #weird left bracket
    "195 167" : "c", #c with tail
    "195 168" : "e", #e with other accent
    "195 169" : "e", #e with accent
    "195 173" : "i", #i with accent
    "195 174" : "i", #i with carrot
    "195 177" : "n", #n with line
    "195 179" : "o", #o with accent
    "195 182" : "oe", #o with umlaut
    "195 184" : "o", #o with slash
    "195 185" : "u", #u with accent
    "195 186" : "a", #a with accent
    "195 187" : "e", #e with accent
    "195 188" : "ue", #u with umlaut
    "196 159" : "g", #g with carrot
    "196 177" : "i", #tiny no-dot i
    "197 147" : "ae", #weird ash
    "197 159" : "s", #s, something turkish
    "197 161" : "s", #s with carrot
    "197 184" : "Y", #Y with umlaut
    "197 189" : "Z", #Z with carrot
    "198 146" : "f", #swoopy f
    "203 156" : "-", #weird high hyphen
    "206 178" : "B", #Esset
    #217 XXX seems to be Arabic
    "226 128 143" : "", #Nothing?
    "226 128 147" : "-", #Weird hyphen
    "226 128 148" : "-", #Weird hyphen
    "226 128 152" : "\'", #Single left quote
    "226 128 153" : "\'", #Single right quote
    "226 128 154" : ",", #Weird comma
    "226 128 156" : "\"", #Double left quote
    "226 128 157" : "\"", #Double right quote
    "226 128 158" : ",", #Double comma
    "226 128 160" : "t", #Cross
    "226 128 166" : "...", #Tiny ellipses
    "226 128 176" : "0/00", #Very strange tiny percentage
    "226 128 178" : "\'", #High right apostrophe 
    "226 130 172" : "E", #Weird Euro sign
    "195 162 226 130 172 226 132 162" : "\'", #apostrophe, encoding problem
    "226 132 162" : "TM", #TM char
    "226 136 154" : "", #Check mark
    "226 150 184" : ">" , #Heavy right arrow
    "226 150 186" : ">" , #Another heavy right arrow
    "226 151 132" : "<" , #Heavy left arrow
    "226 152 128" : "", #Smiley sun face
    "226 152 129" : "", #Storm cloud
    "226 152 130" : "", #Umbrella
    "226 152 131" : "", #Snowing on snowman
    "226 152 148" : "", #Umbrella
    "226 152 149" : "", #Coffee
    "226 152 157" : "", #Single finger hand
    "226 152 186" : "", #Smiley
    "226 153 165" : "", #Heart
    "226 153 186" : "", #Recycle sign
    "226 154 161" : "", #Lightning Bolt
    "226 155 132" : "", #Snowflake?
    "226 156 136" : "", #Plane
    "226 156 139" : "", #Hand
    "226 156 140" : "", #Angry smiley
    "226 156 168" : "", #Can't tell
    "226 157 132" : "", #Snowflake
    "226 157 164" : "", #Heart
    "227 129 175" : "", #Chinese character
    "227 133 139" : "", #Weird double left wind sign something
    "227 133 142" : "", #Circle with hat
    #230 XXX XXX appear to be chinese
    "238 144 139" : "", #Up and left weird arrow
    "238 144 141" : "", #Down and left weird arrow
    "239 191 189" : "?", #Not sure - maybe question mark box?
    "195 131 194 164" : "ae", #Two character a umlaut
    "195 131 194 188" : "ue", #Two characer u umlaut
    "195 131 194 179" : "o", #o with accent
}

def lookup_replacement(chars):
    #Emoji
    if len(chars.split()) == 4 and chars[0:7] == "240 159":
        return "{?}"
    #These appear to be arabic
    elif len(chars.split()) == 2 and chars[0:3] in ["217", "216"]:
        return "{?}"
    #These appear to be chinese
    elif len(chars.split()) == 3 and chars[0:3] == "230":
        return "{?}"
    #Other char in map
    elif chars in CHARACTER_REPLACEMENTS.keys():
        if CHARACTER_REPLACEMENTS[chars] == "":
            return "{?}"
        return CHARACTER_REPLACEMENTS[chars]
    #Couldn't find
    else:
        return None

def fix_characters(line, line_length=False):
    okay = False
    while not okay:
        try:
            line.encode("utf-8")
            okay = True
        except:
            start_point = None
            end_point = None
            bad_chars = 0
            for i in range(len(line)):
                char = line[i]
                try:
                    char.encode("utf-8")
                    if start_point != None and end_point == None:
                        end_point = i
                except:
                    bad_chars += 1
                    if start_point == None:
                        start_point = i

            #In case string is ONLY bad chars
            if start_point != None and end_point == None:
                end_point = len(line)

            if len(line) < 10 or len(line) - bad_chars > len(line) / 1.5:
                replacement = find_replacement(line[start_point:end_point])
                #No replacement found, new char
                if replacement == 1:
                    print line + " " + str(start_point) + " " + str(end_point)
                    replacement = ""
                line = line[0:start_point] + replacement + line[end_point:]
            else:
                print "line mostly crap : " + line
                line = ""
    if line_length:
        return (line, len(line) + bad_chars)
    else:
        return line

def find_replacement(character_string):
    chars = [str(ord(char)) for char in character_string]
    replaced = False
    replacement = ""

    tries = 0
    while len(chars) > 0:
        tries += 1
        all_chars = " ".join(chars).strip()
        
        if all_chars in CHARACTER_REPLACEMENTS.keys():
            replacement += CHARACTER_REPLACEMENTS[all_chars]
            chars = []
        else:
            for i in range(4,0,-1):
                current_chars = " ".join(chars[0:i]).strip()
                current_replacement = lookup_replacement(current_chars)
                if current_replacement != None:
                    replacement += current_replacement 
                    chars = chars[i:]
                    break

        if tries >= 140:
            break

    if len(chars) > 0:
        print "Couldn't replace : " + character_string[3:] + " " + str(chars)
        return 1
    else:
        return replacement


