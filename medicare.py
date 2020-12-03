import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time


url_card = "https://www.medicare.gov/physiciancompare/#results&loc=BROWNSVILLE%2C%20TX%2078526&lat=26.014378&lng=-97.4597725&flow=default&type=specialty&paging=1&keyword=Pain%20Management&previouspage=SG&dist=50&name=Pain%20Management&id=72&practice=solo%2Cahp&loctype=z"

text_file = open("output.txt", "w")
#htfile=open("myhtm.txt","w")
pageno = "4"

# these lines
driver = webdriver.Firefox()
driver.get(url_card)
time.sleep(10)
html = driver.execute_script('return document.documentElement.outerHTML')

#htfile.write(html)

# this is the line
web_soup = BeautifulSoup(html, 'html.parser')

#f = open("myhtm.txt", "r")
#html = f.read()
#web_soup = BeautifulSoup(html, 'html.parser')


# print(web_soup.find_all('strong'))
# print(web_soup.find('strong'))

firstname = []
lastname = []
address = []
city = []
state = []
zipcode = []
telphone = []

group = []
types = []

group_index = []
name_index = []
group_doc=[]
soloindex=[]
group_docIndex=[]
groupsFinal=[]

solofname=[]
sololname=[]
soloaddress=[]
solocity=[]
solostate = []
solozipcode = []
solotelphone = []



class doctor:
    def __init__(self, doc_fname,doc_lname,doc_group,doc_tel,doc_add,doc_city,doc_state,doc_zip,doc_loc):
        self.doc_fname= doc_fname
        self.doc_lname= doc_lname
        self.doc_group= doc_group
        self.doc_tel= doc_tel
        self.doc_add= doc_add
        self.doc_city= doc_city
        self.doc_state= doc_state
        self.doc_zip= doc_zip
        self.doc_loc=doc_loc
    
d_id=[]
doctor_list =[]


def find_offsets(haystack, needle):
    """
    Find the start of all (possibly-overlapping) instances of needle in haystack
    """
    offs = -1
    while True:
        offs = haystack.find(needle, offs+1)
        if offs == -1:
            break
        else:
            yield offs


def getnames():
    print("names\n")
    strong = web_soup.find_all('strong')
    avoid = str(strong[1])
    alsoavoid=str(strong[0])
    for c in range(len(strong)):
        fullname = str(strong[c])
        if fullname != avoid and fullname != alsoavoid:
            group_doc.append(c)
            namelist = fullname.split()
            for myname in namelist:
                if myname == namelist[0]:
                    firstname.append(myname.replace('<strong>', ''))
                if len(namelist) == 2:
                    if myname == namelist[1]:
                        lastname.append(myname.replace('</strong>', ''))
                if len(namelist) == 3:
                    if myname == namelist[1]:
                        lastname.append(
                            namelist[1]+' '+namelist[2].replace('</strong>', ''))
                if len(namelist) == 4:
                    if myname == namelist[1]:
                        lastname.append(namelist[1]+' ' +
                                        namelist[2]+' '+namelist[3].replace('</strong>', ''))
                if len(namelist) == 5:
                    if myname == namelist[1]:
                        lastname.append(namelist[1]+' ' +
                                        namelist[2]+' '+namelist[3]+' '+namelist[4].replace('</strong>', ''))
                if len(namelist) == 6:
                    if myname == namelist[1]:
                        lastname.append(namelist[1]+' ' +
                                        namelist[2]+' '+namelist[3]+' '+namelist[4]+' '+namelist[5].replace('</strong>', ''))
                if len(namelist) == 7:
                    if myname == namelist[1]:
                        lastname.append(namelist[1]+' ' +
                                        namelist[2]+' '+namelist[3]+' '+namelist[4]+' '+namelist[5]+' '+namelist[6].replace('</strong>', ''))

                # print(name[1])
                # for c in name:
                #     if c != name[1] or c == name[0]:
                #         print(c)


def getgroups():
    print("groups\n")

    for txt in web_soup.findAll('a', {'class': 'lv-hospital-link all-caps'}):
        group.append(txt.string)
        print(txt.string)
#stelieto

def gettypes():
    for txt in web_soup.findAll('small'):
        #str_t = str(txt)
        fcut = str(txt)[7:]
        scut = fcut[:-8]
        types.append(scut)


def getgroupindex():
    for offs in find_offsets(html, 'lv-hospital-link all-caps'):
        group_index.append(offs)


def getnameindex():
    for offs in find_offsets(html, '</strong>'):
        name_index.append(offs)


def getaddress():
    print("address\n")


# trim first and last lemnt of the list
# tirm , from then first element
for txt in web_soup.findAll('address'):
    ingram = str(txt)
    fulladd = ingram.split('\n')
    for item in fulladd:
        if item != fulladd[0] and item != fulladd[4]:
            if item == fulladd[1]:
                myaddress = item.replace('<br/>', '').replace(',', '')
                if myaddress[31] == ' ' and myaddress[30] == ' ':
                    address.append(myaddress[32:])
                else:
                    address.append(myaddress[28:])
            if item == fulladd[2]:
                split = item.split(',')
                for value in split:
                    if value == split[0]:
                        ms = value.replace('<br/>', '')
                        if ms[32] == ' ':
                            city.append(ms[33:])
                        else:
                            city.append(ms[29:])

                       # city.append(value.replace('<br/>', '')[33:])
                    if value == split[1]:
                        code = value[:3]
                        zipcode.append(code[1:])
                        shrt = value[4:]
                        state.append(shrt)

            if item == fulladd[3]:
                mynum = item.replace('<br/>', '')
                if mynum[33] == '(':
                    telphone.append(mynum[33:])
                else:
                    telphone.append(mynum[29:])


def printer(data):
    for c in data:
        if c != "Internal" and c != "medicine":
            print(c)


def write_groups():
    for c in range(len(address)):
        text_file.writelines(group[c]+'\t'+address[c]+'\t'+city[c]+'\t' +
                             zipcode[c]+'\t'+state[c]+'\t'+telphone[c]+"\n")

    text_file.close()


def getsolo():
    for c in range(len(types)):
        if types[c] == 'Solo Clinician':
            soloname = group[c]
            namelist = soloname.split()
            for myname in namelist:
                if myname == namelist[0]:
                    solofname.append(myname.replace('<strong>', ''))
                if len(namelist) == 2:
                    if myname == namelist[1]:
                        sololname.append(myname.replace('</strong>', ''))
                if len(namelist) == 3:
                    if myname == namelist[1]:
                        sololname.append(
                            namelist[1]+' '+namelist[2].replace('</strong>', ''))
                if len(namelist) == 4:
                    if myname == namelist[1]:
                        sololname.append(namelist[1]+' ' +
                                        namelist[2]+' '+namelist[3].replace('</strong>', ''))
                if len(namelist) == 5:
                    if myname == namelist[1]:
                        sololname.append(namelist[1]+' ' +
                                        namelist[2]+' '+namelist[3]+' '+namelist[4].replace('</strong>', ''))   
                if len(namelist) == 6:
                    if myname == namelist[1]:
                        sololname.append(namelist[1]+' ' +
                                        namelist[2]+' '+namelist[3]+' '+namelist[4]+' '+namelist[5].replace('</strong>', ''))
                if len(namelist) == 7:
                    if myname == namelist[1]:
                        sololname.append(namelist[1]+' ' +
                                        namelist[2]+' '+namelist[3]+' '+namelist[4]+' '+namelist[5]+' '+namelist[6].replace('</strong>', ''))
                                
            
            soloaddress.append(address[c])
            solocity.append(city[c])
            solozipcode.append(zipcode[c])
            solostate.append(state[c])
            solotelphone.append(telphone[c])
            soloindex.append(group_index[c])

          

            
def pushsolo():
    counter=0
    for c in range(len(types)):
        if types[c]=='Solo Clinician':
            d =  doctor(solofname[counter],sololname[counter],'',solotelphone[counter],soloaddress[counter],solocity[counter],solostate[counter],solozipcode[counter],group_index[counter])
            doctor_list.append(d)
            counter=counter+1




def printclass():
    for c in range(len(doctor_list)):
        print(doctor_list[c].doc_group+'\t'+doctor_list[c].doc_lname+'\t'+doctor_list[c].doc_fname+'\t'+doctor_list[c].doc_add+'\t'+doctor_list[c].doc_city+'\t'+doctor_list[c].doc_state+'\t'+str(doctor_list[c].doc_zip)+'\t'+str(doctor_list[c].doc_tel))


def getGroupDocLOC():
    indexes = group_doc
    for index in sorted(indexes):
        group_docIndex.append(name_index[index])



def assignGroups():
    for c in group_docIndex:
        print(str(c)+" c")
        for g in range(len(group_index)-1,-1,-1):
            print(str(g)+" g")
            if c>group_index[g]:
                groupsFinal.append(group_index[g])
                break    

def group_names():
    for c in range(len(firstname)):
        g=0
        for counter in range(len(group_index)):
            if groupsFinal[c]==group_index[counter]:
                g=counter
        d =  doctor(firstname[c],lastname[c],group[g],telphone[g],address[g],city[g],state[g],zipcode[g],group_docIndex[c])
        doctor_list.append(d)





def printOutput():
    for c in range(len(doctor_list)):
        text_file.writelines(doctor_list[c].doc_group+'\t'+doctor_list[c].doc_lname+'\t'+doctor_list[c].doc_fname+'\t'+doctor_list[c].doc_add+'\t'+doctor_list[c].doc_city+'\t'+str(doctor_list[c].doc_zip)+'\t'+doctor_list[c].doc_state+'\t'+str(doctor_list[c].doc_tel)+'\n')

def sortlist():
    doctor_list.sort(key=lambda x: x.doc_loc)


def printloc():
    for c in range(len(doctor_list)):
        print(str(doctor_list[c].doc_loc))

def printlocsorted():
    for c in range(len(doctor_list)):
        print(str(doctor_list[c].doc_loc))

newlist = sorted(doctor_list, key=lambda x: x.doc_loc, reverse=True)
gettypes()
getgroups()
getnames()
getgroupindex()
getnameindex()
getsolo()
getGroupDocLOC()
assignGroups()
group_names()

# print("==================================================================")
# print(len(soloaddress))
# print(len(solostate))
# print(len(solocity))
# print(len(types))
# print(len(solofname))
# print(len(sololname))
print("==================================================================")
pushsolo()
print("-------------FNAME----------------")
printer(firstname)
print("-------------lastname----------------")
printer(lastname)
print("-------------getaddress----------------")
getaddress()
print("-------------address----------------")
printer(address)
print("-------------city----------------")
printer(city)
print("-------------zipcode----------------")
printer(zipcode)
print("-------------state----------------")
printer(state)
print("-------------telphone----------------")
printer(telphone)


print("-------------types----------------")
printer(types)
print("-------------group_index----------------")
printer(group_index)
print("-------------name_index----------------")
printer(name_index)
print("-------------solofname ----------------")
printer(solofname)
print("-------------sololname----------------")
printer(sololname) 
print("-------------doctor_list----------------")
print(len(doctor_list))
print("-------------group_doc----------------")
printer(group_doc)
print("-------------group_docIndex----------------")
printer(group_docIndex)
print("-------------groupsFinal----------------")
printer(groupsFinal)
print("-------------printclass----------------")
printclass()
print("-------------printclass----------------")
printloc()
print("-------------printclass----------------")
printlocsorted()



#mylist = my_html.find('lv-hospital-link all-caps')
#my_html.findAll('lv-hospital-link all-caps')
#my_html.find_all('lv-hospital-link all-caps')
# print(mylist)


# full = "1817 S D ST, <br/>HEART INSTITUTE AT RENAISSANCE"
# nico = full.replace('<br/>', '')
# print(nico)
#write_groups()
printOutput()
# print(address[2]+','+city[2]+','+zipcode[2]+','+state[2]+','+telphone[2])