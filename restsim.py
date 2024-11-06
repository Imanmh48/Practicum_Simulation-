import random
random.seed() #wanted to fix it first then I will comment this out

         
class Participant:
    def __init__(self,name,score=0): #score set to 0 by default because first time they are registering
        self.name=name
        self.score=score
    
    def apply_score_after_event(self):
        # This is random metrics I have selected for my code to test out
        communication_score=random.randint(1,101)
        communication_weight=random.randint(1,6)
        punctuality_score=random.randint(1,101)
        punctuality_weight=random.randint(1,6)
        incident_respone_score=random.randint(1,101)
        incident_respone_weight=random.randint(1,6)
        total_sum=(communication_score*communication_weight)+(punctuality_score*punctuality_weight)+(incident_respone_score*incident_respone_weight)
        divided_by=incident_respone_weight+punctuality_weight+communication_weight
        self.score+= round(total_sum/divided_by)
def generate_participants():
    participants=[]
    for i in range(1,7):
        participants.append(Participant("v"+str(i)))
    return participants
def apply_reset(list_participants,average): #this will apply the reset for all classes
    for i in list_participants:
        if i.score>=average: #if a volunteer is above the average they get placed back here
            i.score=average
        else:
            i.score-=200 #if they are not the lose X points
    
all_event=50 # in this example the simulation is at 50
#the following code does not apply the reset
participants=generate_participants()
print("="*26)  
#applying the score for each participant
print("Applying the event without reset")

for i in range(all_event):
    for i in participants:
        i.apply_score_after_event()

print("the scores after 50 events")
print("="*26)
#Displaying the score for each pariticipant WITHOUT THE RESET 

avg=0
for i in participants:
    print(i.name+" "+str(i.score))
    avg+=i.score
print("="*26)
print("Average Score:")
print(round(avg/len(participants)))

#in this simulation, every seasons has the same number of events
#The following is when the simulation happens
#generating new participants
new_participants=generate_participants()
print("="*26)
#applying the score for each participant
print("Applying the simulation where seasons have the same number of events")
total=0
for j in new_participants:
            j.apply_score_after_event()
            total+=j.score
avg=round(total/len(new_participants))
the_gap=5
counter=1

for i in range(all_event):
    if i==(counter*all_event)//the_gap:
        print("Season",counter)
        print("-"*26)
        for i in new_participants:
            print(i.name+" "+str(i.score))
        apply_reset(new_participants,avg)
        counter+=1
    else:
        total=0
        for j in new_participants:
            j.apply_score_after_event()
            total+=j.score
        avg=round(total/len(new_participants))
print("-"*26)
print("Season", counter)
for i in new_participants:
    print(i.name+" "+str(i.score))

#In this simulation every seasons has different number of events

event_assignment=[]
# we assume there are 50 events and we are going to distribute them over 4 season 
# each season is 3 months long for example

#while sum(event_assignment)!=all_event: # make sure that my generated number of event is equal to all_events
#    total_event=all_event
#    print("hello")
#    for i in range(4):
#        num_of_event=random.randint(1,all_event) #generate a random number of events
#        event_assignment.append(num_of_event) # append that number

new_participants2=generate_participants()
event_assignment=[]
counter=0
while True: 
    event_assignment=[]
    for i in range(4):
        num_of_event=random.randint(1,all_event) #generate a random number of events
        event_assignment.append(num_of_event) # append that number
    if sum(event_assignment)==all_event: # make sure that my generated number of event is equal to all_events
        print("number of events distribution")
        print(event_assignment)
        break
    counter+=1
    if counter==2000: #safeguard
        print("out")
        break
print("="*26)
print("Applying the simulation where the seasons have different number of events")
total=0
for j in new_participants2:
            j.apply_score_after_event()
            total+=j.score
avg=round(total/len(new_participants2))
current=0
breakpoint=event_assignment[current]
counter=1
for i in range(all_event):
    if i==breakpoint:
        print("Season",counter)
        print("-"*26)
        for i in new_participants2:
            print(i.name+" "+str(i.score))
        apply_reset(new_participants2,avg)
        counter+=1
        current+=1
        breakpoint+=event_assignment[current]
    else:
        total=0
        for j in new_participants2:
            j.apply_score_after_event()
            total+=j.score
        avg=round(total/len(new_participants2))
print("-"*26)
print("Season", counter)
for i in new_participants2:
    print(i.name+" "+str(i.score))