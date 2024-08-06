import requests


def get_difficulty():
    try:
        LINK = input("Problem link: ")
        f = requests.get(LINK)
        ind = f.text.find('title="Difficulty')
        while(f.text[ind] != '*'):
            ind += 1
        ind += 1
        rating = ""
        while(f.text[ind] != '\r'):
            rating += f.text[ind]
            ind += 1
        rating = int(rating)
        difficulties = [1199, 1399, 1599, 1899, 2099, 2399, 10000]
        colors = ["", "\u001b[38;5;10m", "\u001b[38;5;14m",
                "\u001b[38;5;25m", "\u001b[38;5;99m", "\u001b[38;5;3m", "\u001b[38;5;9m"]
        for i in range(len(difficulties)):
            if(rating < difficulties[i]):
                print("Rating: " + '\033[1m' + colors[i] + str(rating))
                break
    except Exception as e:
        print("No rating found")


if(__name__ == "__main__"):
    get_difficulty()
