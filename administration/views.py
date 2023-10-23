from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import requests
from django.contrib.auth.decorators import login_required
from django.conf import settings
from voting.forms import *
from api.serializers import *
from api.models import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django_renderpdf.views import PDFView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta

def find_n_winners(data, n):
    """Read More
    https://www.geeksforgeeks.org/python-program-to-find-n-largest-elements-from-a-list/
    """
    final_list = []
    candidate_data = data[:]
    # print("Candidate = ", str(candidate_data))
    for i in range(0, n):
        max1 = 0
        if len(candidate_data) == 0:
            continue
        this_winner = max(candidate_data, key=lambda x: x['votes'])
        # TODO: Check if None
        this = this_winner['name'] + \
            " with " + str(this_winner['votes']) + " votes"
        final_list.append(this)
        candidate_data.remove(this_winner)
    return ", &nbsp;".join(final_list)


class PrintView(PDFView):
    template_name = 'admin/print.html'
    prompt_download = True

    @property
    def download_name(self):
        return "result.pdf"
    
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)
    

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        context = super().get_context_data(*args, **kwargs)
        position_data = {}
        elections = Election.objects.get(admin=user)
        positions = Position.objects.filter(election_id=elections.id).order_by('priority')
        for position in positions:
            candidate_data = []
            winner = ""
            for candidate in Candidate.objects.filter(position=position):
                this_candidate_data = {}
                votes = Vote.objects.filter(candidate=candidate).count()
                this_candidate_data['name'] = candidate.fullname
                this_candidate_data['votes'] = votes
                candidate_data.append(this_candidate_data)
            if len(candidate_data) < 1:
                winner = "Position does not have candidates"
            else:
                # Check if max_vote is more than 1
                if position.max_vote > 1:
                    winner = find_n_winners(candidate_data, position.max_vote)
                else:

                    winner = max(candidate_data, key=lambda x: x['votes'])
                    if winner['votes'] == 0:
                        winner = "No one voted for this yet position, yet."
                    else:
                        """
                        https://stackoverflow.com/questions/18940540/how-can-i-count-the-occurrences-of-an-item-in-a-list-of-dictionaries
                        """
                        count = sum(1 for d in candidate_data if d.get(
                            'votes') == winner['votes'])
                        if count > 1:
                            winner = f"There are {count} candidates with {winner['votes']} votes"
                        else:
                            winner = "Winner : " + winner['name']
            position_data[position.name] = {
                'candidate_data': candidate_data, 'winner': winner, 'max_vote': position.max_vote}
        
        context['positions'] = position_data
        context['elections'] = position.election
        # print(context)
        return context

# def dashboard(request):
#     #   positions= requests.get('http://127.0.0.1:8000/api/position').json()
#     #   voters= requests.get('http://127.0.0.1:8000/api/voter').json()
#     #   candidates= requests.get('http://127.0.0.1:8000/api/candidate').json()
#     #   votes= requests.get('http://127.0.0.1:8000/api/vote').json()
#       positions = Position.objects.all()
#       voters = Voter.objects.all()
#       candidates = Candidate.objects.all()
#       votes = Vote.objects.all()


#       context = {'positions':positions, 'voters' : voters, 'votes' : votes, 'candidates': candidates}
#       return render(request, 'dashboard.html', context)

def dashboard(request):
    user = request.user
    if user.voter.account_type == 'Admin':
        # positions = Position.objects.all().order_by('priority')
        elections = Election.objects.get(admin=request.user)
        positions = Position.objects.filter(election_id=elections.id).order_by('priority')
        candidates = Candidate.objects.filter(election_id=elections.id).order_by('election')
        voters = Voter.objects.filter(election_id=elections.id).order_by('election')
        voted_elections = Voter.objects.filter(election_id=elections.id)
        voted_voters = voted_elections.filter(voted=1)
        list_of_candidates = []
        votes_count = []
        chart_data = {}

        for position in positions:
            list_of_candidates = []
            votes_count = []
            for candidate in Candidate.objects.filter(position=position):
                list_of_candidates.append(candidate.fullname)
                votes = Vote.objects.filter(candidate=candidate).count()
                votes_count.append(votes)
            chart_data[position] = {
                'candidates': list_of_candidates,
                'votes': votes_count,
                'pos_id': position.id
            }
        # print(chart_data)
        context = {
            'position_count': positions.count(),
            'candidate_count': candidates.count(),
            'voters_count': voters.count(),
            'voted_voters_count': voted_voters.count(),
            'positions': positions,
            'chart_data': chart_data,
        }
    
        return render(request, "admin/admin_home.html", context)
    
    elif user.voter.account_type == 'Voter':
        return render(request, "voter/voter_home.html")
    
    return redirect('account_login')



def viewElections(request):
    user = request.user
    if user.voter.account_type == 'Admin':
        elections = Election.objects.filter(admin=request.user)
        form = ElectionForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                election = form.save(commit=False)
                election.admin = request.user
                election.save()
                messages.success(request, "New Election Created")
            else:
                messages.error(request, "Form errors")

        now = timezone.now() + timedelta(hours=6)
        for election in elections:
            if election.end_date <= now and election.is_open:
                election.is_open = False
                election.save()
                messages.info(request, f"Election '{election.title}' has been closed.")

        context = {
            'elections': elections,
            'form1': form,
        }

        return render(request, 'admin/elections.html', context)

    return redirect('account_login')


def updateElection(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
        return redirect(reverse('viewElections'))

    try:
        election_id = request.POST.get('id')
        election = Election.objects.get(id=election_id)
        if election.admin != request.user:
            messages.error(request, "Access To This Resource Denied")
            return redirect(reverse('viewElections'))

        form = ElectionForm(request.POST, instance=election)
        if form.is_valid():
            if 'end_date' in form.changed_data:
                now = timezone.now() + timedelta(hours=6)
                updated_end_date = form.cleaned_data['end_date']
                # updated_end_date = timezone.make_aware(updated_end_date)
                print(now)
                print(updated_end_date)
                print(updated_end_date<=now)
                if updated_end_date <= now:
                    election.is_open = False
                else:
                    election.is_open = True

            form.save()
            election.save(update_fields=['is_open'])
            messages.success(request, "Election has been updated")
        else:
            messages.error(request, "Form errors")

    except Election.DoesNotExist:
        messages.error(request, "Election not found")
    except:
        messages.error(request, "An error occurred")

    return redirect(reverse('viewElections'))



# def deleteElection(request):
#     election = Election.objects.get(admin=request.user)
#     if request.method != 'POST':
#         messages.error(request, "Access Denied")
#     try:
#         elec = Election.objects.get(id=request.POST.get('id'))
#         elec.delete()
#         messages.success(request, "Election Has Been Deleted")
#         Voter.objects.filter(election=election).update(voted=False)
#     except:
#         messages.error(request, "Access To This Resource Denied")

#     return redirect(reverse('viewElections'))


def deleteElection(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        elec = Election.objects.get(id=request.POST.get('id'))
        # Get all voters associated with the election
        voters = Voter.objects.filter(election=elec)
        # Iterate over the voters
        for voter in voters:
            # If the voter is also an admin, skip the deletion of the voter
            if voter.user.id != elec.admin.id:
                voter.delete()
        messages.success(request, "Voters of Election  Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('viewElections'))


def voters(request):
    user = request.user
    voters_list = Voter.objects.order_by('id') 
    if user.voter.account_type == 'Admin':
        return render(request, 'admin/voters.html', {'voters': voters_list})
    else:
        return redirect('account_login')


def updateVoter(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        instance = Voter.objects.get(id=request.POST.get('id'))
        voter = VoterForm(request.POST or None, instance=instance)
        voter.save()
        messages.success(request, "Voter's bio updated")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('adminViewVoters'))



def view_voter_by_id(request):
    voter_id = request.GET.get('id', None)
    voter = Voter.objects.filter(id=voter_id)
    context = {}
    if not voter.exists():
        context['code'] = 404
    else:
        context['code'] = 200
        voter = voter[0]
        context['verified'] = voter.verified
        context['id'] = voter.id
        previous = VoterForm(instance=voter)
        context['form'] = str(previous.as_p())
    return JsonResponse(context)

def view_election_by_id(request):
    election_id = request.GET.get('id', None)
    election = Election.objects.filter(id=election_id)
    context = {}
    if not election.exists():
        context['code'] = 404
    else:
        context['code'] = 200
        election = election[0]
        context['id'] = election.id
        previous = ElectionForm(instance=election)
        context['form'] = str(previous.as_p())
    return JsonResponse(context)

def view_position_by_id(request):
    pos_id = request.GET.get('id', None)
    pos = Position.objects.filter(id=pos_id)
    context = {}
    if not pos.exists():
        context['code'] = 404
    else:
        context['code'] = 200
        pos = pos[0]
        context['id'] = pos.id
        context['name'] = pos.name
        context['max_vote'] = pos.max_vote
        context['priority'] = pos.priority
    return JsonResponse(context)


def updateVoter(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        instance = Voter.objects.get(id=request.POST.get('id'))
        voter = VoterForm(request.POST or None, instance=instance)
        voter.save()
        messages.success(request, "Voter's bio updated")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('adminViewVoters'))



def deleteVoter(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        admin = Voter.objects.get(id=request.POST.get('id')).user
        admin.delete()
        messages.success(request, "Voter Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('adminViewVoters'))


def viewPositions(request):
    try:
        election = Election.objects.get(admin=request.user)
        positions = Position.objects.filter(election=election)
    except Election.DoesNotExist:
        return redirect('viewElections') 

    form = PositionForm(request.POST or None)
    context = {
        'positions': positions,
        'form1': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            position = form.save(commit=False)
            position.election = election
            position.save()
            messages.success(request, "New Position Created")
            return redirect('viewPositions')
        else:
            messages.error(request, "Form errors")
    return render(request, "admin/positions.html", context)


def updatePosition(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        instance = Position.objects.get(id=request.POST.get('id'))
        pos = PositionForm(request.POST or None, instance=instance)
        pos.save()
        messages.success(request, "Position has been updated")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('viewPositions'))


def deletePosition(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        pos = Position.objects.get(id=request.POST.get('id'))
        pos.delete()
        messages.success(request, "Position Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('viewPositions'))


def viewCandidates(request):
    try:
        election = Election.objects.get(admin=request.user)
        candidates = Candidate.objects.filter(election=election)
    except Election.DoesNotExist:
        return redirect('viewElections') 

    form = CandidateForm(request.POST or None, request.FILES or None)
    context = {
        'candidates': candidates,
        'form1': form,
    }
    if request.method == 'POST':
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.election = election
            candidate.save()
            messages.success(request, "New Candidate Created")
            return redirect('viewCandidates')
        else:
            messages.error(request, "Form errors")
    return render(request, "admin/candidates.html", context)


def updateCandidate(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        candidate_id = request.POST.get('id')
        candidate = Candidate.objects.get(id=candidate_id)
        form = CandidateForm(request.POST or None,
                             request.FILES or None, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, "Candidate Data Updated")
        else:
            messages.error(request, "Form has errors")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('viewCandidates'))


def deleteCandidate(request):
    if request.method != 'POST':
        messages.error(request, "Access Denied")
    try:
        pos = Candidate.objects.get(id=request.POST.get('id'))
        pos.delete()
        messages.success(request, "Candidate Has Been Deleted")
    except:
        messages.error(request, "Access To This Resource Denied")

    return redirect(reverse('viewCandidates'))


def view_candidate_by_id(request):
    candidate_id = request.GET.get('id', None)
    candidate = Candidate.objects.filter(id=candidate_id)
    context = {}
    if not candidate.exists():
        context['code'] = 404
    else:
        candidate = candidate[0]
        context['code'] = 200
        context['fullname'] = candidate.fullname
        previous = CandidateForm(instance=candidate)
        context['form'] = str(previous.as_p())
    return JsonResponse(context)

def ballot_position(request):
    context = {
        'page_title': "Ballot Position"
    }
    return render(request, "admin/ballot_position.html", context)


def update_ballot_position(request, position_id, up_or_down):
    try:
        context = {
            'error': False
        }
        position = Position.objects.get(id=position_id)
        if up_or_down == 'up':
            priority = position.priority - 1
            if priority == 0:
                context['error'] = True
                output = "This position is already at the top"
            else:
                Position.objects.filter(priority=priority).update(
                    priority=(priority+1))
                position.priority = priority
                position.save()
                output = "Moved Up"
        else:
            priority = position.priority + 1
            if priority > Position.objects.all().count():
                output = "This position is already at the bottom"
                context['error'] = True
            else:
                Position.objects.filter(priority=priority).update(
                    priority=(priority-1))
                position.priority = priority
                position.save()
                output = "Moved Down"
        context['message'] = output
    except Exception as e:
        context['message'] = e

    return JsonResponse(context)


def ballot_title(request):
    from urllib.parse import urlparse
    url = urlparse(request.META['HTTP_REFERER']).path
    from django.urls import resolve
    try:
        redirect_url = resolve(url)
        title = request.POST.get('title', 'No Name')
        file = open(settings.ELECTION_TITLE_PATH, 'w')
        file.write(title)
        file.close()
        messages.success(
            request, "Election title has been changed to " + str(title))
        return redirect(url)
    except Exception as e:
        messages.error(request, e)
        return redirect("/")


def viewVotes(request):
    votes = Vote.objects.all()
    context = {
        'votes': votes,
    }
    return render(request, "admin/votes.html", context)


def resetVote(request):
    Vote.objects.all().delete()
    Voter.objects.all().update(voted=False)
    messages.success(request, "All votes has been reset")
    return redirect(reverse('viewVotes'))






