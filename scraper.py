import requests
from bs4 import BeautifulSoup as bs
import gift

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
        gift_rank = text.rstrip()
        gift_camp = "N/A"
        gift_desc = "N/A"
        gift_syst = "N/A"
        gift_src = "N/A"

        prev_entry = "Rank"

        for j in range(1, 6):
            current_text = all_p[i+j].get_text().encode("utf-8").rstrip()
            if prev_entry == "Rank":
                if "Camp:" in current_text:
                    gift_camp = current_text
                    continue

                else:
                    gift_desc = current_text
                    prev_entry = "Desc"
                    continue

            if prev_entry == "Desc":
                if "System:" in current_text:
                    gift_syst = current_text
                    prev_entry = "Syst"
                    continue

                #Catching bad entries that skip 'System:' convention
                elif "Source:" in current_text:
                    print("Expected 'System:' entry found; instead found 'Source:'. Adding current line to Source: {0}".format(current_text))
                    gift_src = current_text
                    break
                else:
                    # print("\n\n-------------- Continuing description --------------\n\n")
                    # print("Gift Desc: " + gift_desc)
                    # print("Continuation: " + current_text)
                    gift_desc = gift_desc + "\n" + current_text
                    continue
            
            if prev_entry == "Syst":
                if "Source:" in current_text:
                    gift_src = current_text
                    prev_entry = "Src"
                    #print(" --------- BREAK! {0} ---------\n\n".format(current_text))
                    break
                else:
                    # print("\n\n-------------- Continuing System --------------\n\n")
                    # print("Gift System: " + gift_syst)
                    # print("Continuation: " + current_text)
                    gift_syst = gift_syst + "\n" + current_text
                    continue

        newgift = gift.Gift("N/A", gift_rank, gift_camp, gift_desc, gift_syst, gift_src)
        giftarr.append(newgift)

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

gift.print_all_gifts(giftarr)