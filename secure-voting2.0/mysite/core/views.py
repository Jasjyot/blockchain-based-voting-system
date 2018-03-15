import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from time import ctime
import hashlib

from .mine import generate_hash
from .models import PollBlockchain, UserProfile

log = logging.getLogger(__name__)
''' @login_required
def home(request):
    return render(request, 'home.html') '''


@login_required
def poll(request):
    log.debug("Hey there it works!!")
    # logging.warning(UserProfile.objects.filter(user=abc).values('isVoteCasted')[0]['isVoteCasted'])
    abc = request.user.username
    if UserProfile.objects.filter(user=abc).values('isVoteCasted')[0]['isVoteCasted']:
        return render(request, 'sucessVote.html')
    else:
        if request.method == 'POST':
            receiverId = request.POST.get('party_name')
            if receiverId != None:
                timeStampVote = str(ctime())
                votesCountInDb = PollBlockchain.objects.count()
                if votesCountInDb != 0:
                    prevHash = PollBlockchain.objects.filter(id=votesCountInDb).values('blockHash')[0]['blockHash']
                    #logging.warning(prevHash)
                else:
                    prevHash = 0

                blockHash, nonce = generate_hash(
                    receiverId, timeStampVote, prevHash)
                # logging.warning("BlockHash:"+blockHash+"\n Nonce:"+str(nonce))
                newBlock = PollBlockchain(receiverId=str(receiverId),
                                        timeStampVote=str(timeStampVote), prevHash=str(prevHash), blockHash=str(blockHash), nonce=str(nonce))
                newBlock.save()

                UserProfile.objects.filter(user=abc).update(isVoteCasted=True)
                #logging.warning(abc)
                return render(request, 'sucessVote.html')

    return render(request, 'poll.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            obj = UserProfile(user=username, isVoteCasted=False)
            obj.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('poll')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def verify(request):

    #receiverId, timestampVote, prevHash, blockHash, nonce are taken from DB for each row
    table = PollBlockchain.objects.values_list('receiverId', 'timeStampVote', 'prevHash', 'blockHash', 'nonce')
    #logging.warning(table)
    numRows= PollBlockchain.objects.count()

    for index, row in enumerate(table):
        concatValue= row[0] + row[1] + row[2] + row[4]
        hash_object = hashlib.sha256(concatValue.encode())
        resultantHash = hash_object.hexdigest()

        #logging.warning(concatValue)
        #logging.warning(resultantHash)
        if resultantHash != row[3]:
            print('Block ' + str(index + 1) + ' of check1 is tamperred')
            return HttpResponse('<h1>Vote has been tampered</h1>')

        if index>0 :
            if table[index - 1][3] != row[2] :
                print('Block ' + str(index + 1) + ' of check2 is tamperred')
                return HttpResponse('<h1>Vote has been tampered</h1>')

    bjpVote= "BJP: "+str(PollBlockchain.objects.filter(receiverId='BJP').count())
    congVote= "CONGRESS: "+str(PollBlockchain.objects.filter(receiverId='CONGRESS').count())
    aapVote= "AAP: "+str(PollBlockchain.objects.filter(receiverId='AAP').count())
    noneVote= "NONE: "+str(PollBlockchain.objects.filter(receiverId='NONE').count())
  
    CountTable = {'content':[bjpVote,congVote,aapVote,noneVote]}
    return render(request,'result.html', CountTable)
