from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

                                            #DATABASE


cluster = MongoClient("mongodb+srv://polingony:UmnASDTkKZfPJvFA@extralearningcluster.drdtq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["e-learning"]
users = db["users"]
courses = db["courses"]
contacts = db["contacts"]
subscription = db["subscription"]
subscriptions = db["subscriptions"]
freemium_users = db["freemium_users"]
freemium_ecd = db["freemium_ecd"]
premium_users = db["premium_users"]
super_users = db["super_users"]

                                            # PLATFORM PROGRAM

app = Flask(__name__)

@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")[:-2]
    res = MessagingResponse()
    user = users.find_one({"number": number})
    usersub = users.find_one({"subscription": subscription})
    fname = user["firstname"]
    sname = user["lastname"]
    fullname = fname + sname
    userfree = freemium_users.find_one({"number": number})
    userpaid = premium_users.find_one({"number": number})

                                            # MAIN STATUS

                                            
    if bool(user) == False:
        mmsg = res.message("Hello and Welcome to *Extra Learning* one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp"
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
        mmsg.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
        users.insert_one({"number": number, "status": "main", "messages": []})

    # Main Status options

    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("Hi To get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            return str(res)

        if option == 1: 
            res.message("   📝 *YOU ARE NOW IN REGISTRATION MODE :*")
            res.message("1️⃣ Primary Education \n\n2️⃣ secondary Education \n\n3️⃣ Courses\n\n4️⃣ About Us \n\n5️⃣ Help \n\n0️⃣ Main Menu")
            users.update_one(
                {"number": number}, {"$set": {"status": "registration"}})
        elif option == 2:
            res.message("   📜 *LOGIN MODE :*")
            users.update_one(
                {"number": number}, {"$set": {"status": "loginpointer"}})
            res.message(
                "You can select one of the following *options* for details: \n\n1️⃣ Primary Education  \n2️⃣ Secondary Education \n3️⃣ Courses"
                "\n4️⃣ About Us \n5️⃣ Help  \n0️⃣ Go Back")
        elif option == 3:
            res.message("   📜 *DEMO MODE :*")
            users.update_one(
                {"number": number}, {"$set": {"status": "demo"}})
            res.message("1️⃣ Primary Education \n\n2️⃣ secondary Education \n\n3️⃣ Courses\n\n4️⃣ Help \n\n0️⃣ Main Menu")

        elif option == 4:
            res.message("   📜 *HELP MODE :*")
            res.message("1️⃣ English \n\n2️⃣ Shona \n\n3️⃣ Contacts \n\n4️⃣ About Us \n\n0️⃣ Main Menu")
            users.update_one(
                {"number": number}, {"$set": {"status": "details"}})
        else:
            res.message("Please enter a *valid* response or use *numbers* to respond in this *mode*"
            "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")