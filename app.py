from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

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
    #usersub = users.find_one({"subscription": subscription})
    #fname = user["firstname"]
    #sname = user["lastname"]
    #fullname = fname + sname
    userfree = freemium_users.find_one({"number": number})
    userpaid = premium_users.find_one({"number": number})


    # Main Checking user is in db

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
            res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
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
            res.message("*_Select level to Register_* \n\n 0️⃣ Programming \n 1️⃣ VID \n 2️⃣ Web Designing \n 3️⃣ Modern Fashion and Fabrics \n 4️⃣ Nurse Aide "
                        " \n 5️⃣ Auto Mechanics \n 6️⃣ Electronics \n 7️⃣ Cyber Security")
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
                {"number": number}, {"$set": {"status": "grade-three-first-name"}})
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

            ecdgomain = res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "ecd", "subscription": "freemium"}})

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

            ecdgomain = res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradeone"}})

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

            ecdgomain = res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradetwo"}})

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

    elif user["status"] == "gradetwo-contact-reg":
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

            ecdgomain = res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradethree"}})


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

            ecdgomain = res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradefour"}})

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

            ecdgomain = res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradefive"}})


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

            ecdgomain = res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradesix"}})

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

            ecdgomain = res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            ecdgomain.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"registration": "gradeseven"}})


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

            # Courses Registering Status and options

    elif user["status"] == "course-registration":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if option == 1:
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
            res.message("   📜 *Web Development Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "wdd-first-name"}})
        elif option == 4:
            res.message("   📜 *Modern Fashion and Fabrics Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "mff-first-name"}})
        elif option == 5:
            res.message("   📜 *Nurse Aid Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "naid-first-name"}})
        elif option == 6:
            res.message("   📜 *Auto Mechanic Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "amm-first-name"}})
        else:
            res.message("Please enter a valid response")

            # About Status and options

    elif user["status"] == "secondary-registration":
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

            # Already Accessed Platform but not registered AANR

    elif user["status"] == "aanr":
        res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ "
                    "Help  \n")
        users.update_one(
            {"number": number}, {"$set": {"status": "main"}})

            #Platform Commands

    elif text == "Extra Learning":
        res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Login \n 2️⃣ Details \n 3️⃣ Demo \n 4️⃣ "
                    "Help  \nTesting Commands")
        users.update_one(
            {"number": number}, {"$set": {"status": "main"}})

            #Content Placeholder

    elif user["status"] == "content":
        res.message("*Extra Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ "
                    "Help  \n")
        users.update_one(
            {"number": number}, {"$set": {"status": "main"}})

            # Login Checking Point
    elif user["status"] == "loginpointer":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        fname = user["firstname"]
        if user["subscription"] == "freemium":
            res.message(f"👋🏼 Hello *{fname}* you're a *_freemium_* user you will have limited content")
            res.message("💻 Enter your _password_ to continue...")
            users.update_one(
            {"number": number}, {"$set": {"status": "loginfree"}})
        elif user["subscription"] == "premium":
            res.message(f"👋🏼 Hello *{fname}* You're a Premium user 🥇")
            users.update_one(
            {"number": number}, {"$set": {"status": "main"}})
        elif bool (user["subscription"]) == False:
            res.message("It looks like you're not registered")
            users.update_one(
            {"number": number}, {"$set": {"status": "main"}})


            # Login Status

    elif user["status"] == "login":
        try:
            bool (userpaid) == True
            fname = user["firstname"]
            level = user["registration"]
        except:
            res.message("It Appears you haven't paid yet..\n\n Contact Admin if you need help")
            res.message("  1️⃣ Register \n 2️⃣ Login \n 3️⃣ Demo \n 4️⃣ Help  \n")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
        if user["password"] == text:
            res.message(f"Hello {fname}, Happy Learning.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
            users.update_one(
                {"number": number}, {"$set": {"status": f"{level}"}})
        else:
            res.message("Wrong Password..\n\n Try again")

            # Freemium User Status

    elif userpaid["status"] == "loginfree":
        fname = user["firstname"]
        pw = user["password"]
        if text == pw:
            level = user["registration"]
            res.message(f"Hello {fname}, Happy Learning.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
            users.update_one(
                {"number": number}, {"$set": {"status": f"{level}"}})
        else:
            res.message("Wrong Password..\n\n Try again")


            # Premium User Status

    elif userpaid["status"] == "loginpaid":
        fname = user["firstname"]
        if text == (userpaid["password"]):
            level = user["registration"]
            res.message(f"Hello {fname}, Happy Learning.\nYou can choose from one of the options below: "
                    "\n\n*Type*\n\n 1️⃣ To *contact* us \n 2️⃣ To *order* snacks \n 3️⃣ To know our *working hours* \n 4️⃣ "
                    "To get our *address*")
            users.update_one(
                {"number": number}, {"$set": {"status": f"{level}"}})
        else:
            res.message("Wrong Password..\n\n Try again")


            # Update Root DB

    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(res)


if __name__ == "__main__":
    app.run()
