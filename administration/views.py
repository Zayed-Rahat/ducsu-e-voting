from django.shortcuts import render,redirect
from voting.models import Position,Voter, Candidate,Notification
from django.contrib.auth.models import User
from voting.forms import PositionForm, VoterForm, CandidateForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

def voters_home(request):
     return render(request, 'voters_home.html')

# def dashboard(request):
#       positions = Position.objects.all()
#       candidates = Candidate.objects.all()
#       voters = User.objects.all() 
#       context = {'positions':positions, 'voters' : voters, 'candidates': candidates}
#       return render(request, 'dashboard.html', context)
def dashboard(request):
    # ... your existing code ...

    # Get notifications for the current user
    positions = Position.objects.all()
    candidates = Candidate.objects.all()
    voters = User.objects.all() 
    notifications = Notification.objects.filter(user=request.user)
    context = {
        'positions': positions,
        'voters': voters,
        'candidates': candidates,
        'notifications': notifications  # Add notifications to the context
    }
    return render(request, 'dashboard.html', context)

# all position showing here


# def position(request):
#     if request.user.username == 'admin':
#         positions_list = Position.objects.order_by('id')  # Order by the 'id' field, you can change it to the desired field
#         paginator = Paginator(positions_list, 5)  # Show 5 positions per page

#         page_number = request.GET.get('page')
#         try:
#             positions = paginator.page(page_number)
#         except PageNotAnInteger:
#             positions = paginator.page(1)
#         except EmptyPage:
#             positions = paginator.page(paginator.num_pages)

#         return render(request, 'position.html', {'positions': positions})
#     else:
#         return redirect('login')
def position(request):
    if request.user.username == 'admin':
        positions_list = Position.objects.order_by('id')  # Order by the 'id' field, you can change it to the desired field
        paginator = Paginator(positions_list, 5)  # Show 5 positions per page

        page_number = request.GET.get('page')
        try:
            positions = paginator.page(page_number)
        except PageNotAnInteger:
            positions = paginator.page(1)
        except EmptyPage:
            positions = paginator.page(paginator.num_pages)

        if request.method == 'POST':
            # Assuming you have a form to add a new position, handle the form submission here
            form = PositionForm(request.POST)
            if form.is_valid():
                new_position = form.save()
                
                # Create a notification when a new position is added
                message = f'New position "{new_position.position_title}" has been added.'
                add_notification(request.user, message)
                
                # Redirect to the position list page
                return redirect('position')
        else:
            form = PositionForm()  # Initialize an empty form for adding new positions
            
        return render(request, 'position.html', {'positions': positions, 'form': form})
    else:
        return redirect('login')

def add_notification(user, message):
    notification = Notification(user=user, message=message)
    notification.save()

    
# Here new position add
def add_position(request):
    user = request.user
    form = PositionForm(request.POST)
    if form.is_valid():
        position = form.save(commit=False)
        position.user = user
        position.save()
        
        # Create a notification when a new position is added
        message = f'New position "{position.position_title}" has been added.'
        add_notification(user, message)
        
        return redirect('position')
    else:
        return render(request, 'add_position.html', {'form': form})

    


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
        voters_list = User.objects.order_by('id')  # Order by the 'id' field, you can change it to the desired field
        paginator = Paginator(voters_list, 5)  # Show 5 voters per page

        page_number = request.GET.get('page')
        try:
            voters = paginator.page(page_number)
        except PageNotAnInteger:
            voters = paginator.page(1)
        except EmptyPage:
            voters = paginator.page(paginator.num_pages)

        return render(request, 'voters.html', {'voters': voters})
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
    
    # if request.user.username == 'admin':
    #     candidates_list = Candidate.objects.all()
    #     paginator = Paginator(candidates_list, 10)  # Show 10 candidates per page

    #     page_number = request.GET.get('page')
    #     try:
    #         candidates = paginator.page(page_number)
    #     except PageNotAnInteger:
    #         # If page is not an integer, default to the first page
    #         candidates = paginator.page(1)
    #     except EmptyPage:
    #         # If page is out of range (e.g. 9999), deliver the last page of results
    #         candidates = paginator.page(paginator.num_pages)

    #     return render(request, 'candidate.html', {'candidates': candidates})
    # else:
    #     return redirect('login')
    
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
    
def add_notification(user, message):
    notification = Notification(user=user, message=message)
    notification.save()
