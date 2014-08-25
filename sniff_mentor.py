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
import sys
from subprocess import Popen, PIPE

signed_pattern = re.compile(".*Signed off by mentor:(.*)")
mentor_tick_pattern = re.compile(".*\[[Xx]{1}\s*\]\s*\([A-Za-z]+\)(.*)")
mentorMap = {}

for line in sys.stdin.readlines():
    spMatch = signed_pattern.match(line)
    mtMatch = mentor_tick_pattern.match(line)
    mentors = []
    mentor = ""

    if spMatch:
        mentor = spMatch.group(1).strip()
    elif mtMatch:
        mentor = mtMatch.group(1).strip()

    if mentor == "":
        continue

    if "," in mentor:
        mentors = mentor.split(",")
    else:
        mentors = [mentor]

    for m in mentors:
        mentorId = None
        m = m.strip()
        if not m in mentorMap:
            if " " in m:
                process = Popen(["./name_to_committer_id.py", m], stdout=PIPE)
                (output, err) = process.communicate()
                exit_code = process.wait()
                if output <> None and output.strip() <> "":
                    mentorId = output.strip()
                else:
                    # one last try, search by last name
                    process2 = Popen(["./name_to_committer_id.py", m.split(" ")[1]], stdout=PIPE)
                    (output2, err2) = process2.communicate()
                    exit_code2 = process2.wait()
                    if output2 <> None and output2.strip() <> "":
                        mentorId = output2.strip()
            else:
                mentorId = m.lower()
        else:
            mentorId = mentorMap[m]
        
        if mentorId <> None:
            mentorMap[m] = mentorId
            print mentorId

