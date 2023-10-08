from django.shortcuts import render, redirect, reverse
from account.views import user_login
from .models import Position, Candidate, Voter, Vote
from django.http import JsonResponse
from django.utils.text import slugify
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse


def generate_ballot(display_controls=False):
    positions = Position.objects.order_by('priority').all()
    output = ""
    candidates_data = ""
    num = 1
    # Initialize instruction with a default value
    instruction = ""

    for position in positions:
        name = position.name
        position_name = slugify(name)
        candidates = Candidate.objects.filter(position=position)
        for candidate in candidates:
            if position.max_vote > 1:
                instruction = f"You may select up to {position.max_vote} candidates"
                input_box = f'<input type="checkbox" value="{candidate.id}" class="flat-red {position_name}" name="{position_name}[]">'
            else:
                instruction = "Select only one candidate"
                input_box = f'<input value="{candidate.id}" type="radio" class="flat-red {position_name}" name="{position_name}">'
            image = f"/media/{candidate.photo}"
            candidates_data += f'''
                <li>
                    {input_box}
                    <button type="button" class="btn btn-primary btn-sm btn-flat clist" data-fullname="{candidate.fullname}" data-bio="{candidate.bio}">
                    </button>
                    <img src="{image}" height="100px" width="100px" class="clist">
                    <span class="cname clist">{candidate.fullname}</span>
                </li>
            '''
        output += f'''
            <div class="row">
                <div class="col-xs-12">
                    <div class="box box-solid" id="{position.id}">
                        <div class="box-header with-border">
                            <h3 class="box-title"><b>{name}</b></h3>
                            {''
                            if display_controls
                            else ''}
                        </div>
                        <div class="box-body">
                            <p>{instruction}
                                <span class="pull-right">
                                    <button type="button" class="btn btn-success btn-sm btn-flat" data-desc="{position_name}">
                                    </button>
                                </span>
                            </p>
                            <div id="candidate_list">
                                <ul>
                                    {candidates_data}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        '''
        position.priority = num
        position.save()
        num += 1
        candidates_data = ''

    return output




def fetch_ballot(request):
    output = generate_ballot(display_controls=True)
    return JsonResponse(output, safe=False)


def show_ballot(request):
    if request.user.voter.voted:
        messages.error(request, "You have voted already")
        return redirect(reverse('myprofile'))
    ballot = generate_ballot(display_controls=False)
    context = {
        'ballot': ballot
    }
    return render(request, "ballot.html", context)


def submit_ballot(request):
    if request.method != 'POST':
        messages.error(request, "Please, browse the system properly")
        return redirect(reverse('show_ballot'))

    # Verify if the voter has voted or not
    voter = request.user.voter
    if voter.voted:
        messages.error(request, "You have voted already")
        return redirect(reverse('myprofile'))

    form = dict(request.POST)
    form.pop('csrfmiddlewaretoken', None)  # Pop CSRF Token
    form.pop('submit_vote', None)  # Pop Submit Button

    # Ensure at least one vote is selected
    if len(form.keys()) < 1:
        messages.error(request, "Please select at least one candidate")
        return redirect(reverse('show_ballot'))
    positions = Position.objects.all()
    form_count = 0
    for position in positions:
        max_vote = position.max_vote
        pos = slugify(position.name)
        pos_id = position.id
        if position.max_vote > 1:
            this_key = pos + "[]"
            form_position = form.get(this_key)
            if form_position is None:
                continue
            if len(form_position) > max_vote:
                messages.error(request, "You can only choose " +
                               str(max_vote) + " candidates for " + position.name)
                return redirect(reverse('show_ballot'))
            else:
                for form_candidate_id in form_position:
                    form_count += 1
                    try:
                        candidate = Candidate.objects.get(
                            id=form_candidate_id, position=position)
                        vote = Vote()
                        vote.candidate = candidate
                        vote.voter = voter
                        vote.position = position
                        vote.save()
                    except Exception as e:
                        messages.error(
                            request, "Please, browse the system properly " + str(e))
                        return redirect(reverse('show_ballot'))
        else:
            this_key = pos
            form_position = form.get(this_key)
            if form_position is None:
                continue
            # Max Vote == 1
            form_count += 1
            try:
                form_position = form_position[0]
                candidate = Candidate.objects.get(
                    position=position, id=form_position)
                vote = Vote()
                vote.candidate = candidate
                vote.voter = voter
                vote.position = position
                vote.save()
            except Exception as e:
                messages.error(
                    request, "Please, browse the system properly " + str(e))
                return redirect(reverse('show_ballot'))
    # Count total number of records inserted
    # Check it viz-a-viz form_count
    inserted_vote = Vote.objects.filter(voter=voter)
    if (inserted_vote.count() != form_count):
        # Delete
        inserted_vote.delete()
        messages.error(request, "Please try voting again!")
        return redirect(reverse('show_ballot'))
    else:
        # Update Voter profile to voted
        voter.voted = True
        voter.save()
        messages.success(request, "Thanks for voting")
        return redirect(reverse('myprofile'))