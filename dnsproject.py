"""
    By: Tremayne Stewart
    DNS Activity Monitor Logger

    Reads a dnslog.txt file that was generated by dns2proxy and outputs a pretty-formatted report of the visited domains and the dns requests associated with visiting them
"""

#Closes the working-domains dnslog entry
#Writes entire working-entry to the file
def closeEntry():
    report = open("report","a")
    global working_domain
    global working_dns
    report.write("%s: %d Time: %s\n" % (working_domain["domain"],len(working_dns),working_domain["timestamp"]))
    ct = 1
    while len(working_dns) > 0:
        report.write("%d.   %s\n" % (ct,working_dns.pop(0)))
        ct+=1
    report.close()


#Extracts the Domain from a dnslog.txt entry
def getDomain(line):
    request_is_index = line.index('request is')
    return line[request_is_index+10:].strip().split(" ")[0].rstrip(".") #Strip Domain Name

#Extracts the timestamp from a dnslog.txt entry
def getTimestamp(line):
    return " ".join(line.split(" ")[:2])

#Closes the previous working-domain's dns logging record and opens a new entry
def addEntry(line):
    global working_domain
    global working_dns
    #Close old entry
    if working_domain:
        closeEntry()
    #format and write to file
    #save new working domain
    working_domain = {
        "domain":getDomain(line),
        "timestamp":getTimestamp(line),
    }


#Add DNS entry to the current working-domain
def addDNS(domain):
    global working_domain
    try:
        if domain == working_domain["domain"]:
            return
        working_dns.index(domain) #Throw error if not in the list
    except:
        working_dns.append(domain)

#Main -----------
dtformat = "%Y-%m-%d %H:%M:%S.%f"
working_domain = None
working_dns =[]

import time
start_time = time.time()

dnslog = open("dnslog.txt","r")
for line in dnslog:
    cur_domain =  getDomain(line)
    if len(cur_domain.split(".")) ==2: # check for name.end
        from datetime import datetime
        if not working_domain:
            addEntry(line)

        #Check if cur domain is diff than working domain and if the access time is at least 45s after
        elif working_domain["domain"]!=cur_domain and \
            (datetime.strptime(getTimestamp(line),dtformat) - datetime.strptime(working_domain["timestamp"],dtformat) ).seconds > 45 :
            addEntry(line)
    else:
        addDNS(cur_domain)

closeEntry() #close the entry when there are no more lines in dnslog.txt

print("--- %s seconds ---" % (time.time() - start_time))
