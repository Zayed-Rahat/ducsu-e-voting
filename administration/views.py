from django.shortcuts import render,redirect
from voting.models import Position,Voter, CustomUser
from voting.forms import PositionForm, VoterForm
from django.contrib.auth.decorators import login_required


def dashboard(request):
    return render(request,'administration/dashboard.html')


# all position showing here
def position(request):
    if request.user.username == 'admin':
      user = request.user
      positions = Position.objects.all() # all position assign to positons for showing
      print(positions)
      return render(request, 'position.html', {'positions':positions})
    else:
        return redirect('login')



# Here new position add
def add_position(request):
    if request.user.username == 'admin':
     user = request.user
     form = PositionForm(request.POST)
     if form.is_valid():
        poses = form.save(commit=False) # position k save kora hocce na
        poses.user = user # request user k assign kora holo
        poses.save() # finaly save kora holo
        return redirect('position')
     else:
        return render(request, 'add_position.html', {'form':form})
    else:
        return redirect('login') 





# position edit here
def edit_position(request, id):
    # if request.user.is_authenticated:
    positions = Position.objects.get(pk=id) #position get form model by using id
    form = PositionForm(instance = positions)
    if request.method == 'POST':
        form = PositionForm(request.POST, instance = positions)
        if form.is_valid():
            form.save()
            return redirect('position') 
    return render(request, 'add_position.html',{'form':form})
    # else:
    #     return redirect('lokgin')
    

# position delete here
def delete_position(request, id):
    # if request.user.is_authenticated:
    positions = Position.objects.get(pk=id) # position get from model using id
    positions.delete()
    return redirect('position')
    # else:
    #     return redirect('add_position')


# all voter showing here
def voters(request):
    if request.user.username == 'admin':
      user = request.user
      voters = CustomUser.objects.all() 
      return render(request, 'voters.html', {'voters':voters})
    else:
        return redirect('login')

# voter edit here
def edit_voters(request, id):
    # if request.user.is_authenticated:
    Voters = CustomUser.objects.get(pk=id) #Voters get form model by using id
    form = VoterForm(instance = Voters)
    if request.method == 'POST':
        form = VoterForm(request.POST, instance = Voters)
        if form.is_valid():
            form.save()
            return redirect('voters') 
    return render(request, 'edit_voters.html',{'form':form})
    # else:
    #     return redirect('login')
    

# Voters delete here
def delete_voters(request, id):
    # if request.user.is_authenticated:
    Voters = CustomUser.objects.get(pk=id) # Voters get from model using id
    Voters.delete()
    return redirect('voters')
    # else:
    #     return redirect('add_Voters')        