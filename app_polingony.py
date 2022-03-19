from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime
import time


#from grade_one_content import *
#import app_text


# Database

cluster = MongoClient("mongodb+srv://polingony:UmnASDTkKZfPJvFA@extralearningcluster.drdtq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = cluster["e-learning"]
users = db["users"]
#students = db["students"]
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
    #student = students.find_one({"number": number})
    #gonedone = res.message(gradeoneweekone())
    #usersub = users.find_one({"subscription": subscription})
    #fullname = fname + sname
    userfree = freemium_users.find_one({"number": number})
    userpaid = premium_users.find_one({"number": number})
    #subs = user["subscription"]
   # usersub = users.find_one({"subscription": f"subs"})
    fmember = users.find_one({"number": number, "registration": "freemium"})
    pmember = users.find_one({"number": number, "registration": "premium"})



    # Main Checking user is in db

    if bool(user) == False:
        mmsg = res.message("Hello and Welcome to *Home Learning* one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp"
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n\n 2️⃣ Login \n\n 3️⃣ Services \n\n 4️⃣ Featured  \n\n 5️⃣ Help")
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
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Services \n 4️⃣ Featured  \n\n 5️⃣ Help")
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
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Services \n 4️⃣ Featured  \n\n 5️⃣ Help ")

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
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Services \n 4️⃣ Featured  \n\n 5️⃣ Help")
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
                        "\n 1️⃣1️⃣ Graphic Designing \n 1️⃣2️⃣ Crypocurrency \n  1️⃣3️⃣ Baking \n 1️⃣4️⃣ Phone Repair \n 1️⃣5️⃣ Electronics"
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
                {"number": number}, {"$set": {"status": "pry-first-name","reglevel": "ecd", "registration": "ECD","subscription": "freemium"}})
        elif option == 1:
            res.message("   📜 *GRADE 1 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-first-name","reglevel": "gradeone", "registration": "GRADE 1","subscription": "freemium"}})
        elif option == 2:
            res.message("   📜 *GRADE 2 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-first-name","reglevel": "gradetwo", "registration": "GRADE 2","subscription": "freemium"}})
        elif option == 3:
            res.message("   📜 *GRADE 3 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-first-name","reglevel": "gradethree", "registration": "GRADE 3","subscription": "freemium"}})
        elif option == 4:
            res.message("   📜 *GRADE 4 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-first-name","reglevel": "gradefour", "registration": "GRADE 4","subscription": "freemium"}})
        elif option == 5:
            res.message("   📜 *GRADE 5 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-first-name","reglevel": "gradefive", "registration": "GRADE 5","subscription": "freemium"}})
        elif option == 6:
            res.message("   📜 *GRADE 6 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-first-name","reglevel": "gradesix", "registration": "GRADE 6","subscription": "freemium"}})
        elif option == 7:
            res.message("   📜 *GRADE 7 Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-first-name","reglevel": "gradeseven", "registration": "GRADE 7","subscription": "freemium"}})
        else:
            res.message("Please enter a valid response")

            # Primary Registering Status (1st Name)

    elif user["status"] == "pry-first-name":
            prygrade = user["registration"]
            res.message(f"   📜 *{prygrade} Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-surname"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # Primary Registering Status (Surname)

    elif user["status"] == "pry-surname":
            prygrade = user["registration"]
            res.message(f"   📜 *{prygrade} Registration :*")
            res.message("Enter *Guardian / Next of kin's Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "pry-guardian"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # Primary Registering Status (Guardian)

    elif user["status"] == "pry-guardian":
            prygrade = user["registration"]
            res.message(f"   📜 *{prygrade} Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # Primary Registering Status (Address)

    elif user["status"] == "pry-address":
            prygrade = user["registration"]
            res.message(f"   📜 *{prygrade} Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-contact"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # Primary Registering Status (contact)

    elif user["status"] == "pry-contact":
            prygrade = user["registration"]
            res.message(f"   📜 *{prygrade} Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # Primary Registering Status (password)

    elif user["status"] == "pry-password":
            fname = user["firstname"]
            sname = user["lastname"]
            cell = user["contact"]
            address = user["address"]
            guardian = user["guardian"]
            huraymsg = res.message("*You are now registered* 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            time.sleep(5.0)
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n"
                        f"Your name is *{fname}* *{sname}*. \n and your Guardian is *{guardian}* " 
                        f"your address for delivery of awards/certificate is *{address}* and contact number is:*{cell}* \n\n" 
                        " 1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "pry-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # Primary Registering Status (Registered)

    elif user["status"] == "pry-registered":

            regdtext = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Services \n 4️⃣ Featured  \n\n 5️⃣ Help")
            regdtext.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})

            



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
                {"number": number}, {"$set": {"status": "sec-first-name","reglevel": "formone", "registration": "FORM 1","subscription": "freemium"}})
        elif option == 2:
            res.message("   📜 *FORM 2 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "sec-first-name","reglevel": "formtwo", "registration": "FORM 2","subscription": "freemium"}})
        elif option == 3:
            res.message("   📜 *FORM 3 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "sec-first-name","reglevel": "formthree", "registration": "FORM 3","subscription": "freemium"}})
        elif option == 4:
            res.message("   📜 *FORM 4 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "sec-first-name","reglevel": "formfour", "registration": "FORM 4","subscription": "freemium"}})
        elif option == 5:
            res.message("   📜 *FORM 5 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "sec-first-name","reglevel": "formfive", "registration": "FORM 5","subscription": "freemium"}})
        elif option == 6:
            res.message("   📜 *FORM 6 :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "sec-first-name","reglevel": "formsix", "registration": "FORM 6","subscription": "freemium"}})
        else:
            res.message("Please enter a valid response")


            # Secondary Registering Status (1st Name)

    elif user["status"] == "sec-first-name":
            secform = user["registration"]
            res.message(f"   📜 *{secform} Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "sec-surname"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # Secondary Registering Status (Surname)

    elif user["status"] == "sec-surname":
            secform = user["registration"]
            res.message(f"   📜 *{secform} Registration :*")
            res.message("Enter *Guardian / Next of kin's Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "sec-guardian"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # Secondary Registering Status (Guardian)

    elif user["status"] == "sec-guardian":
            secform = user["registration"]
            res.message(f"   📜 *{secform} Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "sec-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # Secondary Registering Status (Address)

    elif user["status"] == "sec-address":
            secform = user["registration"]
            res.message(f"   📜 *{secform} Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "sec-contact"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # Secondary Registering Status (contact)

    elif user["status"] == "sec-contact":
            secform = user["registration"]
            res.message(f"   📜 *{secform} Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "sec-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # Secondary Registering Status (password)

    elif user["status"] == "sec-password":
            fname = user["firstname"]
            sname = user["lastname"]
            cell = user["contact"]
            address = user["address"]
            guardian = user["guardian"]
            huraymsg = res.message("*You are now registered* 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            time.sleep(5.0)
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n"
                        f"Your name is *{fname}* *{sname}*. \n and your Guardian is *{guardian}* " 
                        f"your address for delivery of awards/certificate is *{address}* and contact number is:*{cell}* \n\n" 
                        " 1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "sec-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # Secondary Registering Status (Registered)

    elif user["status"] == "sec-registered":

            regdtext = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Services \n 4️⃣ Featured  \n\n 5️⃣ Help")
            regdtext.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})




            # Courses Registering Status and options

    elif user["status"] == "course-registration":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)
        if option == 0:
            res.message("   📜 *MAIN MENU :*")
            res.message(" \n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Services \n 4️⃣ Featured  \n\n 5️⃣ Help")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
        elif option == 1:
            res.message("   📜 *VID Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "vid", "registration": "VID","subscription": "freemium"}})
        elif option == 2:
            res.message("   📜 *Web Designing Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "web-design", "registration": "WEB DESIGNING","subscription": "freemium"}})
        elif option == 3:
            res.message("   📜 *Mushroom Farming Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "mushroom-farming", "registration": "MUSHROOM FARMING","subscription": "freemium"}})
        elif option == 4:
            res.message("   📜 *Modern Fashion and Fabrics Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "fashion-fabrics", "registration": "MODERN FASHION","subscription": "freemium"}})
        elif option == 5:
            res.message("   📜 *Nurse Aide Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "nurse-aide", "registration": "NURSE AIDE","subscription": "freemium"}})
        elif option == 6:
            res.message("   📜 *Auto Mechanics Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "auto-mechanics", "registration": "AUTO MECHANICS","subscription": "freemium"}})
        elif option == 7:
            res.message("   📜 *Make Up Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "make-up", "registration": "MAKE UP","subscription": "freemium"}})
        elif option == 8:
            res.message("   📜 *Hair Dressing Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "hair-dressing", "registration": "HAIR DRESSING","subscription": "freemium"}})
        elif option == 9:
            res.message("   📜 *Modern Decorations Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "modern-deco", "registration": "MODERN DECORATIONS","subscription": "freemium"}})
        elif option == 10:
            res.message("   📜 *Small Business Manegemnt Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "small-business", "registration": "SMALL BUSINESS MANAGEMENT","subscription": "freemium"}})
        elif option == 11:
            res.message("   📜 *Graphic Designing Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "graphicd-first-name","reglevel": "graphic-design", "registration": "GRAPHIC DESIGNING","subscription": "freemium"}})
        elif option == 12:
            res.message("   📜 *Cryptocurency(Bitcoin) Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "crypto", "registration": "CRYPTOCURENCY","subscription": "freemium"}})
        elif option == 13:
            res.message("   📜 *Baking Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "baking", "registration": "BAKING","subscription": "freemium"}})
        elif option == 14:
            res.message("   📜 *Phone Repair Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "phone-repair", "registration": "PHONE REPAIR","subscription": "freemium"}})
        elif option == 15:
            res.message("   📜 *Electronics Registration :*")
            res.message("Please enter *First Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-first-name","reglevel": "electronics", "registration": "ELECTRONICS","subscription": "freemium"}})
        else:
            res.message("Please enter a valid response")


            # COURSE Registering Status (1st Name)

    elif user["status"] == "crs-first-name":
            crsname = user["registration"]
            res.message(f"   📜 *{crsname} Registration :*")
            res.message("\n Enter *Last Name*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-surname"}})
            users.update_one(
                {"number": number}, {"$set": {"firstname": text}})
    
            # COURSE Registering Status (Surname)

    elif user["status"] == "crs-surname":
            crsname = user["registration"]
            res.message(f"   📜 *{crsname} Registration :*")
            res.message("Enter *Guardian / Next of kin's Full Name*")
            users.update_one(
                {"number": number},{"$set": {"status": "crs-guardian"}})
            users.update_one(
                {"number": number}, {"$set": {"lastname": text}})

            # COURSE Registering Status (Guardian)

    elif user["status"] == "crs-guardian":
            crsname = user["registration"]
            res.message(f"   📜 *{crsname} Registration :*")
            res.message("Enter your address")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-address"}})
            users.update_one(
                {"number": number}, {"$set": {"guardian": text}})

            # COURSE Registering Status (Address)

    elif user["status"] == "crs-address":
            crsname = user["registration"]
            res.message(f"   📜 *{crsname} Registration :*")
            res.message("Enter *contact details*")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-contact"}})
            users.update_one(
                {"number": number}, {"$set": {"address": text}})

            # COURSE Registering Status (contact)

    elif user["status"] == "crs-contact":
            crsname = user["registration"]
            res.message(f"   📜 *{crsname} Registration :*")
            res.message("Now Enter your access *Password* that you can remember")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-password"}})
            users.update_one(
                {"number": number}, {"$set": {"contact": text}})

            # COURSE Registering Status (password)

    elif user["status"] == "crs-password":
            fname = user["firstname"]
            sname = user["lastname"]
            cell = user["contact"]
            address = user["address"]
            guardian = user["guardian"]
            huraymsg = res.message("*You are now registered* 🎉✨")
            huraymsg.media("https://i.ibb.co/BPKnXVP/Red-Velvet-Cake-Waldorf-Astoria.jpg")
            time.sleep(5.0)
            res.message("   🎉 *CONGRADULATIONS 🎉 :*\n\n"
                        f"Your name is *{fname}* *{sname}*. \n and your Guardian / Next of Kin is *{guardian}* " 
                        f"your address for delivery of awards/certificate is *{address}* and contact number is:*{cell}* \n\n" 
                        " 1️⃣ *Start :*\n\n")
            users.update_one(
                {"number": number}, {"$set": {"status": "crs-registered"}})
            users.update_one(
                {"number": number}, {"$set": {"password": text}})


            # COURSE Registering Status (Registered)

    elif user["status"] == "crs-registered":

            regdtext = res.message("*Home Learning* is one of the best *e-learning* platform in *Zimbabwe*. "
                "\n\nYou will be learning wherever you are and whenever you want using your Smartphone,Tablet or Personal Computer"
                "using your WhatsApp. \n\n Waiting for your Tutor to wake up or come online is now thing of the past."
                "\n\nTo get Started Respond with the option of your choice using numbers:"
                    "\n\n*Type*\n\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Services \n 4️⃣ Featured  \n\n 5️⃣ Help")
            regdtext.media("http://fdl.polingony.co.zw/pix/el/homelearn.jpg")
            users.update_one(
                {"number": number}, {"$set": {"status": "main"}})
            users.update_one(
                {"number": number}, {"$set": {"day_number":"0","month_number":"0","week_number":"0","sub_duration":"","order_date":""}})


 


            # About Status and options

    elif user["status"] == "about":
        try:
            option = int(text)
        except:
            res.message("Please enter a valid response")
            return str(res)

        if option == 0:
            res.message("   📜 *MAIN MENU :*")
            res.message("\n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Services \n 4️⃣ Featured  \n\n 5️⃣ Help")
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
            res.message(" \n 1️⃣ Register \n 2️⃣ Login \n 3️⃣ Services \n 4️⃣ Featured  \n\n 5️⃣ Help")
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
            level = user["reglevel"]
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
            level = user["reglevel"]
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
