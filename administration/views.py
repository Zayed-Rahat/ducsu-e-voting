from django.shortcuts import render,redirect
from voting.models import Position,Voter, Candidate
from django.contrib.auth.models import User
from voting.forms import PositionForm, VoterForm, CandidateForm

def voters_home(request):
     return render(request, 'voters_home.html')

def dashboard(request):
      positions = Position.objects.all()
      candidates = Candidate.objects.all()
      voters = User.objects.all() 
      context = {'positions':positions, 'voters' : voters, 'candidates': candidates}
      return render(request, 'dashboard.html', context)


# all position showing here
def position(request):
    if request.user.username == 'admin':
      positions = Position.objects.all() # all position assign to positons for showing
      return render(request, 'position.html', {'positions':positions})
    else:
        return redirect('login')
    
# Here new position add
def add_position(request):
     user = request.user
     form = PositionForm(request.POST)
     if form.is_valid():
        poses = form.save(commit=False) # position k save kora hocce na
        poses.user = user # request user k assign kora holo
        poses.save() # finaly save kora holo
        return redirect('position')
     else:
        return render(request, 'add_position.html', {'form':form}) 


# position edit here
def edit_position(request, id):
    positions = Position.objects.get(pk=id) #position get form model by using id
    form = PositionForm(instance = positions)
    if request.method == 'POST':
        form = PositionForm(request.POST, instance = positions)
        if form.is_valid():
            form.save()
            return redirect('position') 
    return render(request, 'add_position.html',{'form':form})
    
# position delete here
def delete_position(request, id):
    positions = Position.objects.get(pk=id) # position get from model using id
    positions.delete()
    return redirect('position')


# all voter showing here
def voters(request):
    if request.user.username == 'admin':
      user = request.user
      voters = User.objects.all() 
      return render(request, 'voters.html', {'voters':voters})
    else:
        return redirect('login')

# voter edit here
def edit_voter(request, id):
    # if request.user.is_authenticated:
    Voters = Voter.objects.get(pk=id) #Voters get form model by using id
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
def delete_voter(request, id):
    # if request.user.is_authenticated:
    Voters = User.objects.get(pk=id) # Voters get from model using id
    Voters.delete()
    return redirect('voters')
    # else:
    #     return redirect('add_Voters')        
    
  
# showing all candidates here 
def show_candidate(request):
    if request.user.username == 'admin':
      candidates = Candidate.objects.all() # all position assign to positons for showing
      return render(request, 'candidate.html', {'candidates':candidates})
    else:
        return redirect('login')
    
    
# candidate add here for vote
def create_candidate(request):
     if request.method == 'POST':
        form = CandidateForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()
            return redirect('candidate')
        else:
            print(form.errors)
     else:
        form = CandidateForm()

     return render(request, 'create_candidate.html', {'form':form}) 
                  
    
# candidate edit function
def edit_candidate(request, id):
    # if request.user.is_authenticated:
    candidate = Candidate.objects.get(pk=id) #candidate get form model by using id
    form = CandidateForm(instance = candidate)
    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            return redirect('candidate') 
    return render(request, 'create_candidate.html',{'form':form})
    # else:
    #     return redirect('lokgin')
    
    
# candidates delete here
def delete_candidate(request, id):
    # if request.user.is_authenticated:
    candidate = Candidate.objects.get(pk=id) # Voters get from model using id
    candidate.delete()
    return redirect('candidate')
    # else:
    #     return redirect('add_Voters')        
    