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

import os
import re
import sys

changesFile = sys.argv[1]
outputFile = sys.argv[2]
relVersion = sys.argv[3]

print "File: "+changesFile

versionChangeLog = {}
version = None
with open(changesFile, 'rb') as cf:
    lines = cf.readlines()
    print "Total lines: "+str(len(lines))
    lineNo = 0
    versionIssues = []
    regex = re.compile(".*\d{1,2}\/\d{1,2}\/\d{4}.*")
    numRegex = re.compile(".*\d{1,2}\..*")
    issueTxt = ""
    for line in lines:
        sline = line.rstrip()
        
        if regex.match(sline):
            if version != None:
                print "Adding version: "+version+" with "+str(len(versionIssues))+" issues "+str(versionIssues)
                versionChangeLog[version] = versionIssues
                versionIssues = []
            
            version = line.rsplit("-")[0].strip()
            print "Version: "+str(version)
            issueTxt = ""
        else:
            if "Release" in line or "notable changes" in line or "----" in line or version == None: 
                continue
            numReg = numRegex.match(line)
            if "*" in line or numReg:
                if numReg:
                    stripDelim = "."
                else:
                    stripDelim = "*"

                if issueTxt != "":
                    versionIssues.append(issueTxt)
                    issueTxt = line.strip()
                    if numReg:
                        issueTxt = issueTxt[issueTxt.find(stripDelim)+1:].strip()
                    else:
                        issueTxt = issueTxt[issueTxt.rfind(stripDelim)+1:].strip()
                else:
                    cleanLine = line.strip()
                    if numReg:
                        cleanLine = cleanLine[cleanLine.find(stripDelim)+1:].strip()
                    else:
                        cleanLine = cleanLine[cleanLine.rfind(stripDelim)+1:].strip()
                    issueTxt = cleanLine
            else:
                issueTxt = issueTxt + line.strip()
                
        lineNo = lineNo + 1
    
# Catch the last version    
if version != None:
    print "Adding version: "+version+" with "+str(len(versionIssues))+" issues "+str(versionIssues)
    versionChangeLog[version] = versionIssues
    versionIssues[:] = []

with open(outputFile, 'w') as of:
    of.write("Apache Tika "+relVersion+"\n\n")
    of.write("\t The most notable changes in Tika "+relVersion+" over the previous release are:\n\n")

    ver = versionChangeLog["Release "+relVersion]

    for issue in ver:
        output = re.sub(r'(?=.*)TIKA\-(\d+)(?=.*)', r'{{{http://issues.apache.org/jira/browse/TIKA-\1}TIKA-\1}}', issue)
        output = re.sub(r'(?=.*)Github\-(\d+)(?=.*)',r'{{{http://github.com/apache/tika/pull/\1}Github-\1}}', output, flags=re.I)
        of.write("\t * "+output+"\n\n")
