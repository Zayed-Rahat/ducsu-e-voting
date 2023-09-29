from django.shortcuts import render,redirect
from voting.models import Position
from voting.forms import PositionForm
from django.contrib.auth.decorators import login_required


def dashboard(request):
    return render(request,'administration/home.html')


# all position showing here
def position(request):
    # if request.user.is_authenticated:
    user = request.user
    positions = Position.objects.all() # all position assign to positons for showing
    return render(request, 'administration/position.html', {'positions':positions})
    # else:
    #     return redirect('login')



# Here new position add
def add_position(request):
    # if request.user.is_authenticated:
    user = request.user
    form = PositionForm(request.POST)
    if form.is_valid():
        poses = form.save(commit=False) # position k save kora hocce na
        poses.user = user # request user k assign kora holo
        poses.save() # finaly save kora holo
        return redirect('position')
    else:
        return render(request, 'administration/add_position.html', {'form':form})





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
    return render(request, 'administration/add_position.html',{'form':form})
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
        