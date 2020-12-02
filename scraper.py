import requests
from bs4 import BeautifulSoup as bs

#Create user-agent to avoid Mod_Security 'Not Acceptable!' error
headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

#request webpage
html_request = requests.get("http://www.wyrmfoe.com/tag/giftrank2/page/1/", headers=headers)

#convert to BeautifulSoup obj
bs_object = bs(html_request.content, 'html.parser')
#print(bs_object.prettify().encode("utf-8"))
#print(bs_object)

# h2 = bs_object.find_all("h2")

# for i in range(len(h2)):
#     giftname = h2[i].get_text().encode("utf-8")
#     print(giftname)

class gift:
    def __init__(self, name, rank, camp, desc, syst, srcbook):
        self.name = name
        self.rank = rank
        self.camp = camp
        self.desc = desc
        self.syst = syst
        self.srcbook = srcbook

#n_gift = gift("newName", "rank", "1", "1", "1", "1")


giftarr = []    #Array containing all gifts found

#Create array containing all <p>
all_p = bs_object.find_all("p")

#Iterate through all text lines except the first text and assemble gifts accordingly
i = 1
while i < len(all_p)-1:
    #print("index: ", i)

    #Grab text from current <p>
    text = all_p[i].get_text().encode("utf-8")
    #print("Text: ", text)
    potential_updated_syst = all_p[i+1].get_text().encode("utf-8")

    #If line containing "System" found then assemble Gift

    if text.startswith("Rank "):

        #print("Gift found!")

        #gift_name = all_p[i-3].get_text().encode("utf-8")
        gift_rank = text
        gift_camp = "N/A"
        gift_desc = "N/A"
        gift_syst = "N/A"
        gift_src = "N/A"

        prev_entry = "Rank"

        for j in range(1, 6):
            current_text = all_p[i+j].get_text().encode("utf-8")
            if prev_entry == "Rank":
                if "Camp:" in current_text:
                    gift_camp = current_text

                else:
                    gift_desc = current_text
                    prev_entry = "Desc"

            if prev_entry == "Desc":
                if "System:" in current_text:
                    gift_syst = current_text
                    prev_entry = "Syst"
                else:
                    gift_desc = gift_desc + "\n" + current_text
            
            if prev_entry == "Syst":
                if "Source:" in current_text:
                    gift_src = current_text
                    prev_entry = "Src"
                else:
                    gift_syst = gift_syst + "\n" + current_text

        
        # gift_syst = text

        # if "Updated" in potential_updated_syst:
        #     gift_updated_syst = potential_updated_syst
        #     gift_sourcebook = all_p[i+2].get_text().encode("utf-8")
        #     #hasUpdatedSys = True
        # else:
        #     gift_updated_syst = "N/A"
        #     gift_sourcebook = potential_updated_syst

        newgift = gift("N/A", gift_rank, gift_camp, gift_desc, gift_syst, gift_src)
        giftarr.append(newgift)

        # print("Gift Desc: ", newgift.desc)
        # print("Gift Syst: ", newgift.syst)
        # print("Gift SrcB: ", newgift.srcbook)

    i+=1


#Add names to gifts
all_h2 = bs_object.find_all("h2")
print("h2: {0} | giftarr: {1}\n".format(len(all_h2), len(giftarr)))

# print("Name: ", all_h2[12].get_text().encode("utf-8"))
# print("Rank: ", giftarr[12].rank)
# print("Camp: ", giftarr[12].camp)
# print("Desc: ", giftarr[12].desc)

if len(all_h2) == len(giftarr):
    for i in range(len(giftarr)):
        giftarr[i].name = all_h2[i].get_text().encode("utf-8")

#     print("NumGifts: ", len(giftarr))
#     for gift in giftarr:
#         print(gift.name)
# else:
#     print("Error: Names and GiftArray len not matching")

if len(all_h2) == len(giftarr):
    print("Successfully scraped gift list of {0} gifts.".format(len(giftarr)))
    print("Attempting to name gifts...")
    for i in range(len(giftarr)):
        giftarr[i].name = all_h2[i].get_text().encode("utf-8")
    print("Gifts successfully named.")
    print("Double checking...")

    check = True
    for i in range(len(giftarr)):
        if giftarr[i].name == "N/A":
            print("Error detected at index {0}. Gift name: {1}".format(i, all_h2[i]))
            check = False
    if check == True:
        print("All gifts named successfully.")
        
else:
    print("Error: Names and GiftArray len not matching")
# print("NumNames: ", len(all_h2))

# for i in range(len(all_h2)):
#     giftname = all_h2[i].get_text().encode("utf-8")
#     print(giftname)

for i in range(len(giftarr)):
    if not giftarr[i].syst.startswith("System:"):
        print("Warning; Entry not starting with 'System: ' detected:")
        print("Name: ", all_h2[i].get_text().encode("utf-8"))
        print("Rank: ", giftarr[i].rank)
        print("Camp: ", giftarr[i].camp)
        print("Desc: ", giftarr[i].desc)
        print("Syst: ", giftarr[i].syst)
        print("Src: ", giftarr[i].srcbook)

"""
def newgift():
    print("New Gift")

def rank():
    print("Rank")

def desc():
    print("Description")

def syst():
    print("System")

def updatedsyst():
    print("Updated System")

def srcbook():
    print("Sourcebook")

switcher = {
    0: newgift,
    1: rank,
    2: desc,
    3: syst,
    4: updatedsyst,
    5: srcbook,
}

switcher.get(0, 1)
"""
        
#for chunk in range(1, len(p)):


#for each <p>, assemble a new gift
# for p in c.find_all("p"):
#     #Get text from the <p>
#     cline = p.get_text().encode("utf-8")

#     #Assemble new gift
#     if search("System: ", cline):
#         print(cline + "\n")

# all_p = bs_object.find_all("p", text=compile("Source:"))

# for i in range(len(all_p)):
#     print(all_p[i])
# print(len(all_p))

"""
for i in range(1, len(p), 4):
    #Rank, Description, System, Source
    print("\n------------- NEW GIFT -------------\n")
    rank = p[i].get_text().encode("utf-8")
    desc = p[i+1].get_text().encode("utf-8")
    syst = p[i+2].get_text().encode("utf-8")
    src = p[i+3].get_text().encode("utf-8")

    print("RANK: %s\n DESC: %s\n SYST: %s\n SRC: %s\n" % (rank, desc, syst, src))
"""
"""
#Find Gift Names
def scrape(weblink, soupobj):
    #convert to BeautifulSoup obj
    c = bs(r.content, 'html.parser')

    #names in h2
    h2 = c.find_all("h2")


    #get all gift names using h2
    for i in range(len(h2)):
        giftname = h2[i].get_text().encode("utf-8")
        print(giftname)
"""