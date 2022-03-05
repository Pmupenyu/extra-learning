#importing time module
import time
import typing

def whatsapp_text(string):
    main_text = "Hello and Welcome to *Home Learning* one of the best *e-learning* platform in *Zimbabwe*. "
    "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
    "using your WhatsApp""\n\nTo get Started Respond with the option of your choice using numbers:"
    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n"
    demo_text = ""
    help_text = "1️⃣ English \n\n2️⃣ Shona \n\n3️⃣ Contacts \n\n4️⃣ About Us \n\n0️⃣ Main Menu"
    

def message(string):
    for i in string:
        #printing each charactor of the message
        print(i, end="")

        #adding time delay of half a second
        time.sleep(0.01)


if __name__=='__main__':
    msg = "It looks like its typing"
    main_text = "Hello and Welcome to *Home Learning* one of the best *e-learning* platform in *Zimbabwe*. "
    "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
    "using your WhatsApp""\n\nTo get Started Respond with the option of your choice using numbers:"
    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n"

    #calling the function for printing the charactors with delay
    message(main_text)
