from django.shortcuts import render, redirect
from bank.models import BloodBank, Blood
from hospital.models import BloodRequest
from bank.forms import BloodBankForm, BloodForm
from django.contrib import messages
from django.http import JsonResponse
from bank.models import City


_INDEX_PAGE = 'index.html'
_LOGIN_PAGE = 'bank/login.html'
_HOME_PAGE = 'bank/home.html'
_ADD_BANK = 'bank/add_bank.html'
_ADD_BLOOD = 'bank/add_blood.html'
_UPDATE_BLOOD = 'bank/update_blood.html'
_REQUESTS_PAGE = 'bank/requests.html'


def index(req):
    return render(req, _INDEX_PAGE)


def logout(req):
    req.session.flush()
    return redirect('home')


def bank_login(req):
    if req.method == 'POST':
        try:
            email = req.POST.get('email')
            password = req.POST.get('password')
            bank = BloodBank.objects.get(email=email, password=password)
            req.session['bank'] = bank.id
            return redirect('bank_home')
        except BloodBank.DoesNotExist:
            return render(req, _LOGIN_PAGE, {'error': 'Invalid Credentials'})
    return render(req, _LOGIN_PAGE)


def home(req):
    bloods = Blood.objects.filter(blood_bank_id=req.session['bank'])
    return render(req, _HOME_PAGE, {'bloods': bloods})


def add_bank(req):
    if req.method == 'POST':
        form = BloodBankForm(req.POST, req.FILES)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect('bank_login')
        else:
            return render(req, _ADD_BANK, {'form': form})
    else:
        form = BloodBankForm()
    return render(req, _ADD_BANK, {'form': form})


def add_blood(req):
    if req.method == 'POST':
        form = BloodForm(req.POST)
        if form.is_valid():
            form.save(commit=False)
            print(req.session['bank'])
            form.instance.blood_bank = BloodBank.objects.get(pk=req.session['bank'])
            form.save()
            return redirect('bank_home')
        else:
            return render(req, _ADD_BLOOD, {'form': form})
    else:
        form = BloodForm()
    return render(req, _ADD_BLOOD, {'form': form})


def update_blood(req, pk):
    if req.method == 'POST':
        blood = Blood.objects.get(pk=pk)
        form = BloodForm(req.POST , instance=blood)
        if form.is_valid():
            form.save()
            return redirect('bank_home')
        else:
            return render(req, _UPDATE_BLOOD, {'form': form})
    else:
        blood = Blood.objects.get(pk=pk)
        form = BloodForm(instance=blood)
    return render(req, _UPDATE_BLOOD, {'form': form})


def delete_blood(req, pk):
    blood = Blood.objects.get(pk=pk)
    blood.delete()
    return redirect('bank_home')


def requests(req):
    bloods = BloodRequest.objects.filter(blood_bank_id=req.session['bank'])
    bloods = bloods.order_by('status')
    # for i in bloods:
    #     i = i.decrypt()
    return render(req, _REQUESTS_PAGE , {'requests': bloods})

def update_request(req, pk):
    blood = BloodRequest.objects.get(pk=pk)
    blood.status = req.GET.get('status')
    blood.save()
    return redirect('bank_requests')

def get_cities(request, state_id):
    cities = City.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(cities), safe=False)


import pickle
def upload(req):
    if req.method=='POST':
        Financial_Year = req.POST['Financial_Year']	
        Branch_Code = req.POST['Branch_Code']	
        Sequence_1 = req.POST['Sequence_1']	
        Sequence_2 = req.POST['Sequence_2']	
        Donation_type = req.POST['Donation_type']	
        Donor_Age = req.POST['Donor_Age']	
        Donation_Date = req.POST['Donation_Date']	
        Gender = req.POST['Gender']	
        Blood_Group_Code = req.POST['Blood_Group_Code']	
        Donor_Weight = req.POST['Donor_Weight']	
        Donor_Temperature = req.POST['Donor_Temperature']	
        Donor_Pulse = req.POST['Donor_Pulse']	
        Donor_Hemoglobin = req.POST['Donor_Hemoglobin']	
        Donor_Blood_Pressure = req.POST['Donor_Blood_Pressure']	
        Test_1 = req.POST['Test_1']	
        Test_2 = req.POST['Test_2']	
        Test_3 = req.POST['Test_3']	
        Test_4 = req.POST['Test_4']
        lee=[Financial_Year,Branch_Code,Sequence_1,Sequence_2,Donation_type,Donor_Age,Donation_Date,Gender,Blood_Group_Code,Donor_Weight,Donor_Temperature,Donor_Pulse,Donor_Hemoglobin,Donor_Blood_Pressure,Test_1,Test_2,Test_3,Test_4]
        filename = (r'decision.sav')
        model = pickle.load(open(filename, 'rb'))
        result =model.predict([lee])
        result=result[0]
        if result==0:
            messages.add_message(req, messages.INFO, "The Person is not Diseased")
            print("The Person is not Diseased")
        else:
            messages.add_message(req, messages.INFO, "The Person is Diseased")
            print("The Person is Diseased")

    return render(req,'upload.html')
    #     accepted_formated=['jpg','png','jpeg','jfif','JPG']
    #     if fn.split('.')[-1] not in accepted_formated:
    #         # flash("Image formats only Accepted","Danger")
    #         return render(req,"upload.html")
    #     new_model = load_model(r"models/mobilenet.h5")
    #     test_image = image.load_img(mypath, target_size=(256, 256))
    #     test_image = image.img_to_array(test_image)
    #     test_image = test_image/255
    #     test_image = np.expand_dims(test_image, axis=0)
    #     result = new_model.predict(test_image)
    #     print(np.argmax(result))
    #     classes=['Actinic Keratosis', 'Basal Cell Carcinoma', 'Dermatofibroma', 'Melanoma', 'Nevus', 'Pigmented Benign Keratosis', 'Seborrheic Keratosis', 'Squamous Cell Carcinoma', 'Vascular Lesion']
    #     prediction=classes[np.argmax(result)]
    #     print(prediction)
    #     if prediction=="Actinic Keratosi":
    #         msg="Actinic Keratosis: This condition is primarily caused by long-term exposure to ultraviolet (UV) light, either from the sun or artificial sources like tanning beds. It's considered a precancerous condition because it can sometimes develop into squamous cell carcinoma."
    #         remedy="Treatment often includes cryotherapy (freezing the lesion), topical creams (like 5-fluorouracil, imiquimod), chemical peels, or laser therapy. The choice of treatment depends on the number and extent of skin lesions."
    #     elif prediction=="Basal Cell Carcinoma":
    #         msg="Basal Cell Carcinoma (BCC): The primary cause of BCC is long-term exposure to UV radiation from the sun or tanning beds. People with fair skin, light hair and eye color, and those with a history of sunburns or excessive sun exposure are at higher risk." 
    #         remedy="Common treatments include surgical excision, Mohs surgery (a precise surgical technique to remove the cancer), cryotherapy, radiation therapy, and topical or oral medications for less invasive types."
    #     elif prediction=="Dermatofibroma":
    #         msg="Dermatofibroma: These benign skin growths can be caused by an injury or insect bite, leading to an overgrowth of fibrous tissue. The exact cause isn't always clear."
    #         remedy="Often, no treatment is necessary unless the lesion is bothersome. Options include surgical removal or cryotherapy if it's painful or growing."
    #     elif prediction=="Melanoma":
    #         msg="Melanoma: The most serious type of skin cancer, melanoma, is largely caused by intense, intermittent UV exposure that leads to sunburns, especially in people with fair skin. Genetic factors and family history also play a role."
    #         remedy="Treatment is dependent on the stage of the cancer and can include surgical removal, immunotherapy, targeted therapy, chemotherapy, and radiation therapy. Early detection and treatment are crucial."
    #     elif prediction=="Nevus":
    #         msg="Nevus (Moles): Moles are usually benign and are caused by a high concentration of melanocytes, the cells that produce pigment in the skin. They can be influenced by genetic factors and sun exposure."
    #         remedy="If a mole is normal and not bothersome, no treatment is needed. If it's suspicious, changing, or cosmetically undesirable, surgical removal is the standard treatment."
    #     elif prediction=="Pigmented Benign Keratosis":
    #         msg="Pigmented Benign Keratosis: These are usually benign growths that are often part of the aging process. Sun exposure can play a role in their development."
    #         remedy="These are usually harmless and don't need treatment unless for cosmetic reasons. Options include cryotherapy, laser therapy, or surgical removal."
    #     elif prediction=="Seborrheic Keratosis":
    #         msg="Seborrheic Keratosis: These growths are common in older adults and may be related to aging, genetic factors, and possibly sun exposure. They're typically benign."
    #         remedy="Treatment is typically not necessary unless the lesions are irritating or for cosmetic reasons. Removal options include cryotherapy, curettage (scraping off the lesion), or laser therapy."
    #     elif prediction=="Squamous Cell Carcinoma":
    #         msg="Squamous Cell Carcinoma (SCC): Like BCC, SCC is mainly caused by cumulative exposure to UV radiation, leading to damage in the DNA of skin cells. People with fair skin, a history of sunburns, or immunosuppression are at increased risk."
    #         remedy="Treatment often involves surgical removal, Mohs surgery, cryotherapy, radiation therapy, or topical chemotherapy, depending on the lesion's size, depth, and location."
    #     else:
    #         msg="Vascular Lesion: This can refer to a range of conditions like hemangiomas or spider veins. Causes can vary widely, from genetic factors to hormonal changes, sun damage, or skin injuries."
    #         remedy="reatment depends on the type of lesion. Options may include laser therapy, sclerotherapy (injection that causes the vessel to collapse), or surgical removal in some cases."

    #     db,cur=data_bace()
    #     ts = time.time()
    #     date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    #     timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    #     sql="insert into disease_info(pname,email,age,gender,smoking,days,infection,bmi,image,disease,severity,causes,remedies,date,time) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #     val=(session['username'],session['useremail'],age,gender,smoking,days,infection,bmi,mypath,prediction,msg1,msg,remedy,date,timeStamp)
    #     cur.execute(sql,val)
    #     db.commit()
    #     sql="select * from doctor"
    #     cur.execute(sql,db)
    #     data=cur.fetchall()
    #     db.commit()
    #     db.close()
    #     return render_template("result.html",image_name=fn, text=prediction,msg=msg , msg1=msg1,data=data)
    # return render_template('upload.html')