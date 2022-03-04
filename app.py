from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime
#from grade_one_content import *
#from app_text import whatsapp_text


# Database

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
    #gonedone = res.message(gradeoneweekone())
    #usersub = users.find_one({"subscription": subscription})
    #fname = user["firstname"]
    #sname = user["lastname"]
    #fullname = fname + sname
    userfree = freemium_users.find_one({"number": number})
    userpaid = premium_users.find_one({"number": number})
    #subs = user["subscription"]
   # usersub = users.find_one({"subscription": f"subs"})



    # Main Checking user is in db

    if bool(user) == False:
        mmsg = res.message("Hello and Welcome to *Home Learning* one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp"
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
        mmsg.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
        users.insert_one({"number": number, "status": "main", "messages": []})
        users.update_one(
                {"number": number}, {"$set": {"subscription":"none"}})
    

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
            res.message("1️⃣ Check")
            users.update_one(
                {"number": number}, {"$set": {"status": "loginpointer"}})
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
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ "
                    "Help  \n")

    # Registering Status and options


    elif user["status"] == "registration":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            users.update_one({"number":number},{"$set": {"status": "main"}})
        elif option == 1:
            res.message("   📜 *PRIMARY EDUCATION :*")
            res.message("*_Select level to Register_* \n\n 0️⃣ ECD \n 1️⃣ Grade 1 \n 2️⃣ Grade 2 \n 3️⃣ Grade 3 \n 4️⃣ Grade 4 "
                        " \n 5️⃣ Grade 5 \n 6️⃣ Grade 6 \n 7️⃣ Grade 7")
            users.update_one(
                {"number": number}, {"$set": {"status": "primary-registration"}})
        elif option == 2:
            res.message("   📜 *SECONDARY EDUCATION :*")
            res.message("*_Select level to Register_* \n\n 1️⃣ Form 1 \n 2️⃣ Form 2 \n 3️⃣ Form 3 \n 4️⃣ Form 4 "
                        " \n 5️⃣ Form 5 \n 6️⃣ Form 6")
            users.update_one(
                {"number": number}, {"$set": {"status": "secondary-registration"}})
        elif option == 3:
            res.message("   📜 *COURSES SECTION :*")
            res.message("*_Select level to Register_* \n\n 0️⃣ Main Menu \n 1️⃣ VID \n 2️⃣ Web Designing \n 3️⃣ Mushroom Farming \n 4️⃣ Modern Fashion "
                        " \n 5️⃣ Nurse Aide \n 6️⃣ Auto Mechanics \n 7️⃣ Make Up\n  8️⃣ Hair Dressing\n 9️⃣ Modern Decorations\n 🔟 Small Business Management"
                        #"\n 1️⃣1️⃣ Graphic Designing \n 1️⃣2️⃣ Crypocurrency \n 1️⃣3️⃣ More to Come"
                        )
            users.update_one(
                {"number": number}, {"$set": {"status": "course-registration"}})
        elif option == 4:
            res.message("   📜 *ABOUT US :*")
            res.message("*_Select option of choice_* \n\n 0️⃣ Main Menu \n 1️⃣ About Platform \n 2️⃣ Contact \n 3️⃣ About us \n 4️⃣ Help ")
            users.update_one(
                {"number": number}, {"$set": {"status": "about"}})
        elif option == 5:
            res.message("   📜 *HELP :*")
            res.message("*_Select option of choice_* \n\n 0️⃣ Main Menu \n 1️⃣ English \n 2️⃣ Shona \n 3️⃣ Ndebele \n 4️⃣ Contact ")
            users.update_one(
                {"number": number}, {"$set": {"status": "help"}})
        else:
            res.message("Please enter a valid response")

        

            # Primary Registering Status and options

    elif user["status"] == "primary-registration":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if option == 0:
            res.message("   📜 *ECD Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "ecd-first-name"}})
        elif option == 1:
            res.message("   📜 *Grade 1 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeone-first-name"}})
        elif option == 2:
            res.message("   📜 *Grade 2 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradetwo-first-name"}})
        elif option == 3:
            res.message("   📜 *Grade 3 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradethree-first-name"}})
        elif option == 4:
            res.message("   📜 *Grade 4 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefour-first-name"}})
        elif option == 5:
            res.message("   📜 *Grade 5 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefive-first-name"}})
        elif option == 6:
            res.message("   📜 *Grade 6 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradesix-first-name"}})
        elif option == 7:
            res.message("   📜 *Grade 7 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeseven-first-name"}})
        else:
            res.message("Please enter a valid response")

            # ECD Registering Status (1st Name)

    elif user["status"] == "ecd-first-name":
            res.message("   📜 *ECD Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "ecd-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # ECD Registering Status (Surname)

    elif user["status"] == "ecd-surname-name":
            res.message("   📜 *ECD Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "ecd-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # ECD Registering Status (Guardian)

    elif user["status"] == "ecd-guardian-name":
            res.message("   📜 *ECD Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # ECD Registering Status (Address)

    elif user["status"] == "address":
            res.message("   📜 *ECD Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "ecd-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # ECD Registering Status (contact)

    elif user["status"] == "ecd-contact-reg":
            res.message("   📜 *ECD Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "ecd-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # ECD Registering Status (password)

    elif user["status"] == "ecd-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            ecdregmsg = res.message("You are now registered 🎉✨")
            ecdregmsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "ecd-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # ECD Registering Status (Registered)

    elif user["status"] == "ecd-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "ecd", "subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})

            # GRADE 1 Registering Status (1st Name)

    elif user["status"] == "gradeone-first-name":
            res.message("   📜 *GRADE 1 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeone-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # GRADE 1 Registering Status (Surname)

    elif user["status"] == "gradeone-surname-name":
            res.message("   📜 *GRADE 1 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "gradeone-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # GRADE 1 Registering Status (Guardian)

    elif user["status"] == "gradeone-guardian-name":
            res.message("   📜 *GRADE 1 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeone-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # GRADE 1 Registering Status (Address)

    elif user["status"] == "gradeone-address":
            res.message("   📜 *GRADE 1 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeone-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # GRADE 1 Registering Status (contact)

    elif user["status"] == "gradeone-contact-reg":
            res.message("   📜 *GRADE 1 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeone-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # GRADE 1 Registering Status (password)

    elif user["status"] == "gradeone-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeone-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # GRADE 1 Registering Status (Registered)

    elif user["status"] == "gradeone-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradeone","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})

            # GRADE 2 Registering Status (1st Name)

    elif user["status"] == "gradetwo-first-name":
            res.message("   📜 *GRADE 2 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradetwo-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # GRADE 2 Registering Status (Surname)

    elif user["status"] == "gradetwo-surname-name":
            res.message("   📜 *GRADE 2 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "gradetwo-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # GRADE 2 Registering Status (Guardian)

    elif user["status"] == "gradetwo-guardian-name":
            res.message("   📜 *GRADE 2 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradetwo-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # GRADE 2 Registering Status (Address)

    elif user["status"] == "gradetwo-address":
            res.message("   📜 *GRADE 2 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradetwo-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # GRADE 2 Registering Status (contact)

    elif user["status"] == "gradetwo-contact-reg":
            res.message("   📜 *GRADE 2 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradetwo-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # GRADE 2 Registering Status (password)

    elif user["status"] == "gradetwo-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradetwo-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # GRADE 2 Registering Status (Registered)

    elif user["status"] == "gradetwo-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradetwo","subscription": "freemium"}})

            # GRADE 3 Registering Status (1st Name)

    elif user["status"] == "gradethree-first-name":
            res.message("   📜 *GRADE 3 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradethree-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # GRADE 3 Registering Status (Surname)

    elif user["status"] == "gradethree-surname-name":
            res.message("   📜 *GRADE 3 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "gradethree-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # GRADE 3 Registering Status (Guardian)

    elif user["status"] == "gradethree-guardian-name":
            res.message("   📜 *GRADE 3 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradethree-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # GRADE 3 Registering Status (Address)

    elif user["status"] == "gradetwo-address":
            res.message("   📜 *GRADE 3 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradethree-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # GRADE 3 Registering Status (contact)

    elif user["status"] == "gradethree-contact-reg":
            res.message("   📜 *GRADE 3 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradethree-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # GRADE 3 Registering Status (password)

    elif user["status"] == "gradethree-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradethree-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # GRADE 3 Registering Status (Registered)

    elif user["status"] == "gradethree-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradethree","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


            # GRADE 4 Registering Status (1st Name)

    elif user["status"] == "gradefour-first-name":
            res.message("   📜 *GRADE 4 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefour-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # GRADE 4 Registering Status (Surname)

    elif user["status"] == "gradefour-surname-name":
            res.message("   📜 *GRADE 4 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "gradefour-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # GRADE 4 Registering Status (Guardian)

    elif user["status"] == "gradefour-guardian-name":
            res.message("   📜 *GRADE 4 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefour-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # GRADE 4 Registering Status (Address)

    elif user["status"] == "gradefour-address":
            res.message("   📜 *GRADE 4 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefour-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # GRADE 4 Registering Status (contact)

    elif user["status"] == "gradefour-contact-reg":
            res.message("   📜 *GRADE 4 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefour-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # GRADE 4 Registering Status (password)

    elif user["status"] == "gradefour-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefour-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # GRADE 4 Registering Status (Registered)

    elif user["status"] == "gradefour-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradefour","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})

            # GRADE 5 Registering Status (1st Name)

    elif user["status"] == "gradefive-first-name":
            res.message("   📜 *GRADE 5 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefive-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # GRADE 5 Registering Status (Surname)

    elif user["status"] == "gradefive-surname-name":
            res.message("   📜 *GRADE 5 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "gradefive-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # GRADE 5 Registering Status (Guardian)

    elif user["status"] == "gradefive-guardian-name":
            res.message("   📜 *GRADE 5 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefive-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # GRADE 5 Registering Status (Address)

    elif user["status"] == "gradefive-address":
            res.message("   📜 *GRADE 5 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefive-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # GRADE 5 Registering Status (contact)

    elif user["status"] == "gradefive-contact-reg":
            res.message("   📜 *GRADE 5 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefive-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # GRADE 5 Registering Status (password)

    elif user["status"] == "gradefive-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradefive-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # GRADE 5 Registering Status (Registered)

    elif user["status"] == "gradefive-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradefive","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


            # GRADE 6 Registering Status (1st Name)

    elif user["status"] == "gradesix-first-name":
            res.message("   📜 *GRADE 6 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradesix-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # GRADE 6 Registering Status (Surname)

    elif user["status"] == "gradesix-surname-name":
            res.message("   📜 *GRADE 6 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "gradesix-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # GRADE 6 Registering Status (Guardian)

    elif user["status"] == "gradesix-guardian-name":
            res.message("   📜 *GRADE 6 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradesix-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # GRADE 6 Registering Status (Address)

    elif user["status"] == "gradesix-address":
            res.message("   📜 *GRADE 6 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradesix-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # GRADE 6 Registering Status (contact)

    elif user["status"] == "gradesix-contact-reg":
            res.message("   📜 *GRADE 6 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradesix-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # GRADE 6 Registering Status (password)

    elif user["status"] == "gradesix-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradesix-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # GRADE 6 Registering Status (Registered)

    elif user["status"] == "gradesix-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradesix","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})

            # GRADE 7 Registering Status (1st Name)

    elif user["status"] == "gradeseven-first-name":
            res.message("   📜 *GRADE 7 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeseven-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # GRADE 7 Registering Status (Surname)

    elif user["status"] == "gradeseven-surname-name":
            res.message("   📜 *GRADE 7 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "gradeseven-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # GRADE 7 Registering Status (Guardian)

    elif user["status"] == "gradeseven-guardian-name":
            res.message("   📜 *GRADE 7 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeseven-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # GRADE 7 Registering Status (Address)

    elif user["status"] == "gradeseven-address":
            res.message("   📜 *GRADE 7 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeseven-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # GRADE 7 Registering Status (contact)

    elif user["status"] == "gradeseven-contact-reg":
            res.message("   📜 *GRADE 7 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeseven-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # GRADE 7 Registering Status (password)

    elif user["status"] == "gradeseven-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "gradeseven-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # GRADE 7 Registering Status (Registered)

    elif user["status"] == "gradeseven-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradeseven","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


            # Secondary Registering Status and options

    elif user["status"] == "secondary-registration":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if option == 0:
            res.message("   📜 *Main Menu :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
        elif option == 1:
            res.message("   📜 *FORM 1 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formone-first-name"}})
        elif option == 2:
            res.message("   📜 *FORM 2 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formtwo-first-name"}})
        elif option == 3:
            res.message("   📜 *FORM 3 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formthree-first-name"}})
        elif option == 4:
            res.message("   📜 *FORM 4 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfour-first-name"}})
        elif option == 5:
            res.message("   📜 *FORM 5 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfive-first-name"}})
        elif option == 6:
            res.message("   📜 *FORM 6 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formsix-first-name"}})
        else:
            res.message("Please enter a valid response")


            # FORM 1 Registering Status (1st Name)

    elif user["status"] == "formone-first-name":
            res.message("   📜 *FORM 1 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formone-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # FORM 1 Registering Status (Surname)

    elif user["status"] == "formone-surname-name":
            res.message("   📜 *FORM 1 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "formone-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # FORM 1 Registering Status (Guardian)

    elif user["status"] == "formone-guardian-name":
            res.message("   📜 *FORM 1 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "formone-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # FORM 1 Registering Status (Address)

    elif user["status"] == "formone-address":
            res.message("   📜 *FORM 1 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formone-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # FORM 1 Registering Status (contact)

    elif user["status"] == "formone-contact-reg":
            res.message("   📜 *FORM 1 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "formone-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # FORM 1 Registering Status (password)

    elif user["status"] == "formone-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "formone-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # FORM 1 Registering Status (Registered)

    elif user["status"] == "formone-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "formone","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


            # FORM 2 Registering Status (1st Name)

    elif user["status"] == "formtwo-first-name":
            res.message("   📜 *FORM 2 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formtwo-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # FORM 2 Registering Status (Surname)

    elif user["status"] == "formtwo-surname-name":
            res.message("   📜 *FORM 2 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "formtwo-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # FORM 2 Registering Status (Guardian)

    elif user["status"] == "formtwo-guardian-name":
            res.message("   📜 *FORM 2 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "formtwo-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # FORM 2 Registering Status (Address)

    elif user["status"] == "formtwo-address":
            res.message("   📜 *FORM 2 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formtwo-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # FORM 2 Registering Status (contact)

    elif user["status"] == "formtwo-contact-reg":
            res.message("   📜 *FORM 2 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "formtwo-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # FORM 2 Registering Status (password)

    elif user["status"] == "formtwo-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "formtwo-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # FORM 2 Registering Status (Registered)

    elif user["status"] == "formtwo-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "formtwo","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


            # FORM 3 Registering Status (1st Name)

    elif user["status"] == "formthree-first-name":
            res.message("   📜 *FORM 3 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formthree-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # FORM 3 Registering Status (Surname)

    elif user["status"] == "formthree-surname-name":
            res.message("   📜 *FORM 3 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "formthree-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # FORM 3 Registering Status (Guardian)

    elif user["status"] == "formthree-guardian-name":
            res.message("   📜 *FORM 3 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "formthree-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # FORM 3 Registering Status (Address)

    elif user["status"] == "formthree-address":
            res.message("   📜 *FORM 3 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formthree-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # FORM 3 Registering Status (contact)

    elif user["status"] == "formthree-contact-reg":
            res.message("   📜 *FORM 3 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "formthree-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # FORM 3 Registering Status (password)

    elif user["status"] == "formthree-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "formthree-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # FORM 3 Registering Status (Registered)

    elif user["status"] == "formthree-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "formthree","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


            # FORM 4 Registering Status (1st Name)

    elif user["status"] == "formfour-first-name":
            res.message("   📜 *FORM 4 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfour-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # FORM 4 Registering Status (Surname)

    elif user["status"] == "formfour-surname-name":
            res.message("   📜 *FORM 4 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "formfour-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # FORM 4 Registering Status (Guardian)

    elif user["status"] == "formfour-guardian-name":
            res.message("   📜 *FORM 4 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfour-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # FORM 4 Registering Status (Address)

    elif user["status"] == "formfour-address":
            res.message("   📜 *FORM 4 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfour-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # FORM 4 Registering Status (contact)

    elif user["status"] == "formfour-contact-reg":
            res.message("   📜 *FORM 4 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfour-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # FORM 4 Registering Status (password)

    elif user["status"] == "formfour-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfour-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # FORM 4 Registering Status (Registered)

    elif user["status"] == "formfour-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "formfour","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


            # FORM 5 Registering Status (1st Name)

    elif user["status"] == "formfive-first-name":
            res.message("   📜 *FORM 5 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfive-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # FORM 5 Registering Status (Surname)

    elif user["status"] == "formfive-surname-name":
            res.message("   📜 *FORM 5 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "formfive-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # FORM 5 Registering Status (Guardian)

    elif user["status"] == "formfive-guardian-name":
            res.message("   📜 *FORM 5 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfive-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # FORM 5 Registering Status (Address)

    elif user["status"] == "formfive-address":
            res.message("   📜 *FORM 5 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfive-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # FORM 5 Registering Status (contact)

    elif user["status"] == "formfive-contact-reg":
            res.message("   📜 *FORM 5 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfive-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # FORM 5 Registering Status (password)

    elif user["status"] == "formfive-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "formfive-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # FORM 5 Registering Status (Registered)

    elif user["status"] == "formfive-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "formfive","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


            # FORM 6 Registering Status (1st Name)

    elif user["status"] == "formsix-first-name":
            res.message("   📜 *FORM 6 Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formsix-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # FORM 6 Registering Status (Surname)

    elif user["status"] == "formsix-surname-name":
            res.message("   📜 *FORM 6 Registration :*")
            res.message("Enter *Guardian Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "formsix-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # FORM 6 Registering Status (Guardian)

    elif user["status"] == "formsix-guardian-name":
            res.message("   📜 *FORM 6 Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "formsix-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # FORM 6 Registering Status (Address)

    elif user["status"] == "formsix-address":
            res.message("   📜 *FORM 6 Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "formsix-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # FORM 6 Registering Status (contact)

    elif user["status"] == "formsix-contact-reg":
            res.message("   📜 *FORM 6 Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "formsix-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # FORM 6 Registering Status (password)

    elif user["status"] == "formsix-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "formsix-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # FORM 6 Registering Status (Registered)

    elif user["status"] == "formsix-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "formsix","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})




            # Courses Registering Status and options

    elif user["status"] == "course-registration":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            res.message("   📜 *MAIN MENU :*")
            res.message(" 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
        elif option == 1:
            res.message("   📜 *VID Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "vid-first-name"}})
        elif option == 2:
            res.message("   📜 *Web Designing Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "wd-first-name"}})
        elif option == 3:
            res.message("   📜 *Mushroom Farming Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "wdd-first-name"}})
        elif option == 4:
            res.message("   📜 *Modern Fashion and Fabrics Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "mff-first-name"}})
        elif option == 5:
            res.message("   📜 *Nurse Aide Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "nurse-aide-first-name"}})
        elif option == 6:
            res.message("   📜 *Auto Mechanics Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "amm-first-name"}})
        elif option == 7:
            res.message("   📜 *Make Up Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "makeup-first-name"}})
        elif option == 8:
            res.message("   📜 *Hair Dressing Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "hairdressing-first-name"}})
        elif option == 9:
            res.message("   📜 *Modern Decorations Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "deco-first-name"}})
        elif option == 10:
            res.message("   📜 *Small Business Manegemnt Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "deco-first-name"}})
        elif option == 11:
            res.message("   📜 *Graphic Designing Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "graphicd-first-name"}})
        elif option == 12:
            res.message("   📜 *Cryptocurrency(Bitcoin) Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crypto-first-name"}})
        elif option == 13:
            res.message("   📜 *Baking Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "baking-first-name"}})
        elif option == 14:
            res.message("   📜 *Phone Repair Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "phonerepair-first-name"}})
        elif option == 15:
            res.message("   📜 *Electronics Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "electonics-first-name"}})
        else:
            res.message("Please enter a valid response")

            # VID Registering Status (1st Name)

    elif user["status"] == "vid-first-name":
            res.message("   📜 *VID Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "vid-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # VID Registering Status (Surname)

    elif user["status"] == "vid-surname-name":
            res.message("   📜 *VID Registration :*")
            res.message("Enter *Guardian / Next of kin's Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "vid-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # VID Registering Status (Guardian)

    elif user["status"] == "vid-guardian-name":
            res.message("   📜 *VID Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "vid-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # VID Registering Status (Address)

    elif user["status"] == "vid-address":
            res.message("   📜 *VID Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "vid-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # VID Registering Status (contact)

    elif user["status"] == "vid-contact-reg":
            res.message("   📜 *VID Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "vid-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # VID Registering Status (password)

    elif user["status"] == "vid-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "vid-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # VID Registering Status (Registered)

    elif user["status"] == "vid-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "vid","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})
            

            # VID Registering Status (1st Name)

    elif user["status"] == "graphicd-first-name":
            res.message("   📜 *Graphic Designing Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "graphicd-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # VID Registering Status (Surname)

    elif user["status"] == "graphicd-surname-name":
            res.message("   📜 *Graphic Designing Registration :*")
            res.message("Enter *Guardian / Next of kin's Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "graphicd-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # VID Registering Status (Guardian)

    elif user["status"] == "graphicd-guardian-name":
            res.message("   📜 *Graphic Designing Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "graphicd-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # VID Registering Status (Address)

    elif user["status"] == "graphicd-address":
            res.message("   📜 *Graphic Designing Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "graphicd-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # VID Registering Status (contact)

    elif user["status"] == "graphicd-contact-reg":
            res.message("   📜 *Graphic Designing Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "graphicd-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # VID Registering Status (password)

    elif user["status"] == "graphicd-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "graphicd-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # VID Registering Status (Registered)

    elif user["status"] == "vid-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "graphicd","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


            # Web Designing  Registering Status (1st Name)

    elif user["status"] == "wd-first-name":
            res.message("   📜 *Web Designing  Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "wd-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # Web Designing  Registering Status (Surname)

    elif user["status"] == "wd-surname-name":
            res.message("   📜 *Web Designing  Registration :*")
            res.message("Enter *Guardian / Next of kin's Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "wd-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # Web Designing  Registering Status (Guardian)

    elif user["status"] == "wd-guardian-name":
            res.message("   📜 *Web Designing  Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "wd-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # Web Designing  Registering Status (Address)

    elif user["status"] == "wd-address":
            res.message("   📜 *Web Designing  Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "wd-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # Web Designing  Registering Status (contact)

    elif user["status"] == "wd-contact-reg":
            res.message("   📜 *Web Designing  Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "wd-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # Web Designing  Registering Status (password)

    elif user["status"] == "wd-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "wd-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # Web Designing  Registering Status (Registered)

    elif user["status"] == "wd-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "webdesigning","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})

            # MUSHROOM FARMING Registering Status (1st Name)

    elif user["status"] == "mushroom-first-name":
            res.message("   📜 *MUSHROOM FARMING Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "mushroom-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # MUSHROOM FARMING Registering Status (Surname)

    elif user["status"] == "mushroom-surname-name":
            res.message("   📜 *MUSHROOM FARMING Registration :*")
            res.message("Enter *Guardian / Next of kin's Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "mushroom-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # MUSHROOM FARMING Registering Status (Guardian)

    elif user["status"] == "mushroom-guardian-name":
            res.message("   📜 *MUSHROOM FARMING Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "mushroom-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # MUSHROOM FARMING Registering Status (Address)

    elif user["status"] == "mushroom-address":
            res.message("   📜 *MUSHROOM FARMING Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "mushroom-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # MUSHROOM FARMING Registering Status (contact)

    elif user["status"] == "mushroom-contact-reg":
            res.message("   📜 *MUSHROOM FARMING Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "mushroom-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # MUSHROOM FARMING Registering Status (password)

    elif user["status"] == "mushroom-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "mushroom-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # MUSHROOM FARMING Registering Status (Registered)

    elif user["status"] == "mushroom-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "mushroom","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})



            # MODERN FASHION AND FABRICS Registering Status (1st Name)

    elif user["status"] == "modern-fashion-first-name":
            res.message("   📜 *MODERN FASHION AND FABRICS Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "modern-fashion-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # MODERN FASHION AND FABRICS Registering Status (Surname)

    elif user["status"] == "modern-fashion-surname-name":
            res.message("   📜 *MODERN FASHION AND FABRICS Registration :*")
            res.message("Enter *Guardian / Next of kin's Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "modern-fashion-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # MODERN FASHION AND FABRICS Registering Status (Guardian)

    elif user["status"] == "modern-fashion-guardian-name":
            res.message("   📜 *MODERN FASHION AND FABRICS Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "modern-fashion-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # MODERN FASHION AND FABRICS Registering Status (Address)

    elif user["status"] == "modern-fashion-address":
            res.message("   📜 *MODERN FASHION AND FABRICS Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "modern-fashion-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # MODERN FASHION AND FABRICS Registering Status (contact)

    elif user["status"] == "modern-fashion-contact-reg":
            res.message("   📜 *MODERN FASHION AND FABRICS Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "modern-fashion-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # MODERN FASHION AND FABRICS Registering Status (password)

    elif user["status"] == "modern-fashion-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "modern-fashion-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # MODERN FASHION AND FABRICS Registering Status (Registered)

    elif user["status"] == "modern-fashion-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "modern-fashion","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


            # NURSE AIDE Registering Status (1st Name)

    elif user["status"] == "nurse-aide-first-name":
            res.message("   📜 *NURSE AIDE Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "nurse-aide-surname-name"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # NURSE AIDE Registering Status (Surname)

    elif user["status"] == "nurse-aide-surname-name":
            res.message("   📜 *NURSE AIDE Registration :*")
            res.message("Enter *Guardian / Next of kin's Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "nurse-aide-guardian-name"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # NURSE AIDE Registering Status (Guardian)

    elif user["status"] == "nurse-aide-guardian-name":
            res.message("   📜 *NURSE AIDE Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "nurse-aide-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # NURSE AIDE Registering Status (Address)

    elif user["status"] == "nurse-aide-address":
            res.message("   📜 *NURSE AIDE Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "nurse-aide-contact-reg"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # NURSE AIDE Registering Status (contact)

    elif user["status"] == "nurse-aide-contact-reg":
            res.message("   📜 *NURSE AIDE Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "nurse-aide-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # NURSE AIDE Registering Status (password)

    elif user["status"] == "nurse-aide-password":
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n")
            huraymsg = res.message("You are now registered 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            startmsg = res.message("   1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "nurse-aide-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # NURSE AIDE Registering Status (Registered)

    elif user["status"] == "nurse-aide-registered":

            ecdgomain = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Demo \n\n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "nurse-aide","subscription": "freemium","day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})




            # About Status and options

    elif user["status"] == "about":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if option == 0:
            res.message("   📜 *MAIN MENU :*")
            res.message(" 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            users.update_one(
                {"number": number}, {"$set": {"status": "primary-registration"}})
        elif option == 1:
            res.message("   📜 *FORM 1 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "primary-registration"}})
        elif option == 2:
            res.message("   📜 *FORM 2 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "secondary-registration"}})
        elif option == 3:
            res.message("   📜 *FORM 3 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "course-registration"}})
        elif option == 4:
            res.message("   📜 *FORM 4 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "about"}})
        elif option == 5:
            res.message("   📜 *FORM 5 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "help"}})
        elif option == 6:
            res.message("   📜 *FORM 6 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "about"}})
        else:
            res.message("Please enter a valid response")

            # Help Status and options

    elif user["status"] == "help":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if option == 0:
            res.message("   📜 *MAIN MENU :*")
            res.message("  1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
        elif option == 1:
            res.message("   📜 *FORM 1 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "help-enlish"}})
        elif option == 2:
            res.message("   📜 *FORM 2 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "help-shona"}})
        elif option == 3:
            res.message("   📜 *FORM 3 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "help-ndebele"}})
        elif option == 4:
            res.message("   📜 *FORM 4 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "contact"}})
        elif option == 5:
            res.message("   📜 *FORM 5 :*")
            res.message("Please enter your address to confirm the order")
            users.update_one(
                {"number": number}, {"$set": {"status": "help-adress"}})
        else:
            res.message("Please enter a valid response")



            # Login Checking Point
    elif user["status"] == "loginpointer":
        
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if user["subscription"] == "freemium":
            fname = user["firstname"]
            res.message(f"👋🏼 Hello *{fname}* you're a *_freemium_* user you will have limited content")
            res.message("💻 Enter your _password_ to continue...")
            users.update_one(
            {"number": number}, {"$set": {"status": "loginfree"}})
        elif user["subscription"] == "premium":
            fname = user["firstname"]
            res.message(f"👋🏼 Hello *{fname}* You're a Premium user 🥇")
            res.message("💻 Enter your _password_ to continue...")
            users.update_one(
            {"number": number}, {"$set": {"status": "main"}})
        elif user["subscription"] == "none":
            res.message("*It looks like you're not registered*\n\n *You are now being taken to Registration mode* \n\n\n📝 *YOU ARE NOW IN REGISTRATION MODE :*")
            res.message("1️⃣ Primary Education \n\n2️⃣ secondary Education \n\n3️⃣ Courses\n\n4️⃣ About Us \n\n5️⃣ Help \n\n0️⃣ Main Menu")
            users.update_one(
                {"number": number}, {"$set": {"status": "registration"}})



            # Freemium User Status

    elif user["status"] == "loginfree":
        psw = text
        fname = user["firstname"]
        if psw == user["password"]:
            level = user["registration"]
            res.message(f"Hello *{fname}*, and Happy Learning.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To pay for *Premium* \n\n 2️⃣ For free 1 Week _Learning_ \n\n 3️⃣ To Learn how it _works_ \n\n 4️⃣ "
                    "To get _assistance_")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
        else:
            res.message("Wrong Password..😒\n\n Try again")


            # Premium User Status

    elif user["status"] == "loginpaid":
        psw = text
        fname = user["firstname"]
        if psw == user["password"]:
            level = user["registration"]
            res.message(f"Hello {fname}, and Happy Learning.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To Start *Learning* \n\n 2️⃣ For _Balance Enquiry_ \n\n 3️⃣ To Learn how it _works_ \n\n 4️⃣ "
                    "To get _assistance_ \n\n5️⃣ Syllabus")
            users.update_one(
                {"number": number}, {"$set": {"status": f"{level}"}})
        else:
            res.message("Wrong Password..😒\n\n Try again")


            # Update Root DB

    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()
