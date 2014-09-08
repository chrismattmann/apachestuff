#!/usr/bin/env python
# encoding: utf-8
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 

import re
import urllib2
import sys
import unicodedata
import string

people_url = "http://people.apache.org/committer-index.html"
name = unicode(sys.argv[1], "utf-8")
name_toks = name.split(" ")
namePattern = ""
selectMentorIdPattern = ".*id\=\'([a-z0-9]+)\'.*"
selectMentorIdCompiled = re.compile(selectMentorIdPattern)

# source:
# http://stackoverflow.com/questions/20729827/compare-2-strings-without-considering-accents-in-python
def remove_accents(data):
    return ''.join(x for x in unicodedata.normalize('NFKD', data) if x in string.ascii_letters).lower()

if " " not in name:
    namePattern = ".*\>"+remove_accents(name.lower())+"\<.*"
else:
    name_toks = re.split('\s+|\-',name)
    namePattern = ".*\>"

    for tok in name_toks:
        if (len(tok) == 1 or len(tok) == 2 and "." in tok) and len(name_toks) == 3:
            namePattern = namePattern+"("+remove_accents(tok.lower())+")*\s*[A-Za-z.\-]*\s*"
        else:
            # total hack
            replaced=False
            if tok == "Dave":
                tok = u"(David|Dave)"
                replaced=True
            elif tok == "Matt":
                tok = u"(Matthew|Matt)"
                replaced=True
            elif tok == "Tom":
                tok = u"(Tom|Thomas)"
                replaced=True
            elif tok == "Henri":
                tok = u"(Gomez|Henri)"
                replaced=True
            elif tok == "Gomez":
                tok = u"(Henri|Gomez)"
                replaced=True
            elif tok == "Mike":
                tok = u"(Mike|Michael)"
                replaced=True
            elif tok == "Fromm":
                continue # skip due to Isabel still being listen under maiden name
            elif tok == "O'Malley":
                replaced=True # hack so this doesn't get accents removed
            elif tok == "Pietro":
                continue # skip due to not being included by his last name.
            elif tok == "Tomaz":
                tok = u"(Tomaž|Tomaz)"      
                replaced=True
            elif tok == "Afkham":
                tok = u"(Mohamed Afkham)"
                replaced=True

            if replaced:
                namePattern = namePattern+tok.lower()+"\s*[A-Za-z.\-]*\s*"
            else:
                namePattern = namePattern+remove_accents(tok.lower())+"\s*[A-Za-z.\-]*\s*"
    namePattern = namePattern + ".*\<"

namePatternCompiled = re.compile(namePattern)
prevLine = ""
theMatch=""
for line in urllib2.urlopen(people_url).readlines():
    if namePatternCompiled.match(unicode(line.lower(), "utf-8")) and prevLine <> None and prevLine.find("<tr>") == -1:
        mentorIdMatch = selectMentorIdCompiled.match(prevLine)
        if mentorIdMatch:
            theMatch = mentorIdMatch.group(1).strip().lower()

    prevLine = line.lower()

# take the last match    
if theMatch <> None and theMatch.strip() <> "":
    print theMatch.strip()
