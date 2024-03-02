from django.shortcuts import redirect, render
from hospital.forms import HospitalForm, BedForm,BloodRequestForm
from hospital.models import Bed,Hospital,BloodRequest
from bank.models import Blood

_LOGIN_PAGE = 'hospital/login.html'
_HOME_PAGE = 'hospital/home.html'
_ADD_HOSPITAL = 'hospital/add_hospital.html'
_ADD_BED = 'hospital/add_bed.html'
_UPDATE_BED = 'hospital/update_bed.html'
_REQUESTS_PAGE = 'hospital/requests.html'
_RAISE_REQUESTS_PAGE = 'hospital/raise_request.html'

def hospital_login(req):
    if req.method == 'POST':
        try:
            email = req.POST.get('email')
            password = req.POST.get('password')
            hospital = Hospital.objects.get(email=email, password=password)
            print(hospital or 'not found')
            req.session['hospital'] = hospital.id
            return redirect('hospital_home')
        except Hospital.DoesNotExist:
            return render(req, _LOGIN_PAGE , {'error': 'Invalid Credentials'})
    return render(req, _LOGIN_PAGE)

def home(req):
    beds = Bed.objects.filter(hospital_id = req.session['hospital'])
    return render(req, _HOME_PAGE , {'beds': beds})

def add_hospital(req):
    if req.method == 'POST':
        form = HospitalForm(req.POST , req.FILES)
        if form.is_valid():
            form.save()
            return redirect('hospital_login')
        else:
            return render(req, _ADD_HOSPITAL, {'form': form})
    else:
        form = HospitalForm()
    return render(req, _ADD_HOSPITAL, {'form': form})


def add_bed(req):
    if req.method == 'POST':
        form = BedForm(req.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.hospital = Hospital.objects.get(pk=req.session['hospital'])
            form.save()
            return redirect('hospital_home')
        else:
            return render(req, _ADD_BED, {'form': form})
    else:
        form = BedForm()
    return render(req, _ADD_BED, {'form': form})


def update_bed(req , pk):
    if req.method == 'POST':
        bed = Bed.objects.get(pk=pk)
        form = BedForm(req.POST, instance=bed)
        if form.is_valid():
            form.save()
            return redirect('hospital_home')
        else:
            return render(req, _UPDATE_BED, {'form': form})
    else:
        bed = Bed.objects.get(pk=pk)
        form = BedForm(instance=bed)
    return render(req, _UPDATE_BED, {'form': form})


def delete_bed(req, pk):
    bed = Bed.objects.get(pk=pk)
    bed.delete()
    return redirect('hospital_home')

def requests(req):
    requests = BloodRequest.objects.filter(hospital_id=req.session['hospital'])
    # for i in requests:
    #     i = i.decrypt()
    return render(req, _REQUESTS_PAGE, {'requests': requests})

def delete_request(req, pk):
    request = BloodRequest.objects.get(pk=pk)
    request.delete()
    return redirect('requests')


def raise_request(req):
    if req.method == 'POST':
        form = BloodRequestForm(req.POST)
        print(req.session['hospital'])
        if form.is_valid():
            form.save(commit=False)
            form.instance.hospital = Hospital.objects.get(pk=req.session['hospital'])
            form.save() 
        else:
            return render(req, _RAISE_REQUESTS_PAGE, {'form': form})
        return redirect('requests')
    else:
        form = BloodRequestForm()
        bloods = Blood.objects.all()
        return render(req, _RAISE_REQUESTS_PAGE , {'form': form , "bloods": bloods})