from weather import *
from bitcoin_curr import *

salutations = ("bonjour", "salut", "hey", "yo", "wesh")

def classify(msg):
    msg = msg.lower().strip()
    if msg == "help":
       return "Je sais répondre aux salutations basiques ainsi que vous donner la météo :)"
    if msg in salutations:
       return "Bonjour ! Comment est votre blanquette ?"
    if msg.find("bitcoin") == 0:
        try:
            currency = msg.split()[1]
            return bitcoin(currency)
        except:
            return "Tktbitcoin"
    if msg.find("euros") == 0:
        try:
            currency = msg.split()[1]
            return bitcoin(currency, invert=True)
        except:
            return "Tktbitcoin"
    if msg.find("weather") == 0:
    	try:
    	    city = msg.split()[1]
    	    return weather(city)
    	except:
    	    return "Je ne connais pas cette ville, désolé"
    return "Pardon, je n'ai pas compris"

# Vous permet de tester votre bot directement dans le terminal
if __name__ == "__main__":
    try:
        while (1):
            msg = input("Message: ")
            print(classify(msg))
    except (EOFError, KeyboardInterrupt):
        print("\nAu revoir !")
