from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient, mongo_client
from datetime import datetime

# Database

cluster = MongoClient("mongodb+srv://polingony:UmnASDTkKZfPJvFA@extralearningcluster.drdtq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["e-learning"]
users = db["users"]
courses = db["courses"]
contacts = db["contacts"]
subscription = db["subscription"]
subscriptions = db["subscriptions"]
demo_users = db["demo_users"]
freemium_users = db["freemium_users"]
premium_users = db["premium_users"]
super_users = db["super_users"]
# Primary Database
grade_one = db["grade_one"]
grade_two = db["grade_two"]
grade_three = db["grade_three"]
grade_four = db["grade_four"]
grade_five = db["grade_five"]
grade_six = db["grade_six"]
grade_seven = db["grade_seven"]
# Secondary Database
form_one = db["form_one"]
form_two = db["form_two"]
form_three = db["form_three"]
form_four = db["form_four"]
form_five = db["form_five"]
form_six = db["form_six"]
# Duration Database
day_one = db["day_one"]

register_mode = db["register_mode"]
details_mode = db["register_mode"]
help_mode = db["help_mode"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:", "")[:-2]
    res = MessagingResponse()
    user = users.find_one({"number": number})

    # Main Checking user is in db

    if bool(user) == False:
        mmsg = res.message("Hello and Welcome to *Extra Learning* one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp"
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Details \n 3️⃣ Demo \n 4️⃣ "
                    "Help  \n")
        mmsg.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
        users.insert_one({"number": number, "status": "main", "messages": []})

    # Main Status options

    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            res.message("To get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Details \n 3️⃣ Demo \n 4️⃣ "
                    "Help  \n")
            return str(res)

        if option == 1:
            res.message("   📝 *YOU ARE NOW IN REGISTRATION MODE*;")
            res.message("1️⃣ Primary Education \n\n2️⃣ secondary Education \n\n3️⃣ Courses\n\n4️⃣ About Us \n\n5️⃣ Help \n\n0️⃣ Main Menu")
            register_mode.update_one(
                {"number": number}, {"$set": {"status": "registration"}})
        elif option == 2:
            res.message("   📜 *DETAILS MODE*;")
            details_mode.update_one(
                {"number": number}, {"$set": {"status": "details"}})
            res.message(
                "You can select one of the following cakes to order: \n\n1️⃣ Primary Education  \n2️⃣ Secondary Education \n3️⃣ Courses"
                "\n4️⃣ About Us \n5️⃣ Help  \n0️⃣ Go Back")
        elif option == 3:
            res.message("   📜 *DEMO MODE*;")
            demo_users.update_one(
                {"number": number}, {"$set": {"status": "demo"}})
            res.message("1️⃣ Primary Education \n\n2️⃣ secondary Education \n\n3️⃣ Courses\n\n4️⃣ Help \n\n0️⃣ Main Menu")

        elif option == 4:
            res.message("   📜 *HELP MODE*;")
            res.message("1️⃣ English \n\n2️⃣ Shona \n\n3️⃣ Contacts \n\n4️⃣ About Us \n\n0️⃣ Main Menu")
            help_mode.update_one(
                {"number": number}, {"$set": {"status": "details"}})
        else:
            res.message("Please enter a *valid* response or use *numbers* to respond in this *mode*"
            "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Details \n 3️⃣ Demo \n 4️⃣ "
                    "Help  \n")


    # Registering Status and options


    elif user["status"] == "registration":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            users.update_one(
                {"number": number}, {"*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Details \n 3️⃣ Demo \n 4️⃣ "
                    "Help  \n"},
                    {"$set": {"status": "main"}})
        elif option == 1:
            res.message("   📜 *PRIMARY EDUCATION*;")
            res.message("Please enter your address to confirm the order")
            register_mode.update_one(
                {"number": number}, {"$set": {"status": "primary-registration"}})
        elif option == 2:
            res.message("   📜 *SECONDARY EDUCATION*;")
            res.message("Please enter your address to confirm the order")
            register_mode.update_one(
                {"number": number}, {"$set": {"status": "secondary-registration"}})
        elif option == 3:
            res.message("   📜 *COURSES SECTION*;")
            res.message("Please enter your address to confirm the order")
            register_mode.update_one(
                {"number": number}, {"$set": {"status": "course-registration"}})
        elif option == 4:
            res.message("   📜 *ABOUT US*;")
            res.message("Please enter your address to confirm the order")
            register_mode.update_one(
                {"number": number}, {"$set": {"status": "about"}})
        elif option == 5:
            res.message("   📜 *HELP*;")
            res.message("Please enter your address to confirm the order")
            register_mode.update_one(
                {"number": number}, {"$set": {"status": "help"}})
        else:
            res.message("Please enter a valid response")

            # Primary Registering Status and options

    elif user["status"] == "primary-registration":
        selected = user["item"]
        rmsg = res.message("Thanks for shopping with us 😊")
        rmsg.message(f"Your order for *{selected}* has been received and will be delivered within an hour")
        register_mode.insert_one({"number": number, "item": selected, "address": text, "order_time": datetime.now()})
        users.update_one(
            {"number": number}, {"$set": {"status": "ordered"}})
    elif user["status"] == "registered":
        res.message(f"Hello {freemium_users.__full_name}, Happy Learning.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
        users.update_one(
            {"number": number}, {"$set": {"status": "login"}})
    freemium_users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)

if __name__ == "__main__":
    app.run()
