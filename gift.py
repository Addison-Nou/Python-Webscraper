class Gift:
    def __init__(self, name="N/A", rank="N/A", camp="N/A", desc="N/A", syst="N/A", book="N/A", will=0, rage=0, passive=False):
        self.name = name #Gift Name
        self.rank = rank #Gift Rank
        self.camp = camp #Camp Origin
        self.desc = desc #Gift Description
        self.syst = syst #System function
        self.book = book #Source book
        self.will = will #Bool spend Willpower
        self.rage = rage #Bool spend Rage
        self.passive = passive #Bool passive Gift

def print_all_gifts(giftArr):
    """
    giftArr[gift1, gift2, ...]
    gift1.name = ""
    ...
    """

    for i in range(len(giftArr)):
        v = vars(giftArr[i])
        #print(v)
        for j in v:
            print("{} : {}".format(j, v[j]))
        print("\n")
        # for key in giftArr[i]:
        #     print("{0}".format(key))

#Finds all Tribes listed in the gift
def find_tribe(gift):
    tribes = gift.rank.split(" / ")
    print("Tribes: {0}".format(tribes))
