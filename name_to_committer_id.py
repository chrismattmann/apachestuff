#!/usr/bin/env python
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

people_url = "http://people.apache.org/committer-index.html"
name = sys.argv[1]
name_toks = name.split(" ")
namePattern = ""
selectMentorIdPattern = ".*id\=\'([a-z0-9]+)\'.*"
selectMentorIdCompiled = re.compile(selectMentorIdPattern)

if " " not in name:
    namePattern = ".*\>"+name.lower()+"\<.*"
else:
    name_toks = name.split(" ")
    namePattern = ".*\>"
    for tok in name_toks:
        if len(tok) == 1 and len(name_toks) == 3:
            namePattern = namePattern+"("+tok.lower()+")*\s*[A-Za-z.]*\s*"
        else:
            # total hack
            if tok == "Dave":
                tok = "Dav[e]{0,1}[i]{0,1}[d]{0,1}"
            elif tok == "Matt":
                tok = "Matt[h]{0,1}[e]{0,1}[w]{0,1}"
            elif tok == "Tom":
                tok = "(Thomas)*(Tom)*"
            elif tok == "Henri":
                tok = "Gomez"
            elif tok == "Gomez":
                tok = "Henri"

            namePattern = namePattern+tok.lower()+"\s*[A-Za-z.]*\s*"
    namePattern = namePattern + ".*\<"

namePatternCompiled = re.compile(namePattern)
prevLine = ""
theMatch=""
for line in urllib2.urlopen(people_url).readlines():
    if namePatternCompiled.match(line.lower()) and prevLine <> None and prevLine.find("<tr>") == -1:
        mentorIdMatch = selectMentorIdCompiled.match(prevLine)
        theMatch = mentorIdMatch.group(1).strip().lower()

    prevLine = line.lower()

# take the last match    
if theMatch <> None and theMatch.strip() <> "":
    print theMatch.strip()
