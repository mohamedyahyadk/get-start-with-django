from django.core.mail import send_mail 

from django.shortcuts import render ,redirect
from django.http import HttpResponse
from leads.models import Lead ,Agent
from .forms import LeadForm ,LeadModelForm ,CustomUserCreationForm
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView  ,ListView ,DetailView ,CreateView ,UpdateView ,DeleteView

# 
from agents.mixins import OrganisorAndLoginRequiredMixin


class SignupView(CreateView):
     template_name="registration/signup.html"
     form_class=CustomUserCreationForm
     success_url='/login'





class LandingPageView(TemplateView):
    template_name='landing.html'

def landing_page(request):
      return render(request,'landing.html')


class  LeadListView(LoginRequiredMixin,ListView):
     template_name="leads/lead_list.html"
     context_object_name='leads'
     def get_queryset(self):
         user=self.request.user
         # initial queryset of leads for the entire organisation 
         if user.is_organisor:
          queryset=Lead.objects.filter(organisation=user.userprofile)
         else  :
               queryset=Lead.objects.filter(organisation=user.agent.organisation)
               # filter based on if the user is agent 
               queryset=Lead.objects.filter(agent__user=user)
         return queryset

def lead_list(request):
  leads=Lead.objects.all()
  context={
    "leads":leads
  }
  return render(request,"leads/lead_list.html",context)



class  LeadDetailtView(LoginRequiredMixin,DetailView):
     template_name="leads/lead_detail.html"
     context_object_name='lead'
     def get_queryset(self):
         user=self.request.user
         # initial queryset of leads for the entire organisation 
         if user.is_organisor:
          queryset=Lead.objects.filter(organisation=user.userprofile)
         else  :
               queryset=Lead.objects.filter(organisation=user.agent.organisation)
               # filter based on if the user is agent 
               queryset=Lead.objects.filter(agent__user=user)
         return queryset


def lead_detail(request,pk):

    lead=Lead.objects.get(id=pk)
    context={
    "lead":lead
  }
    return render(request,"leads/lead_detail.html",context)



class  LeadCreateView(OrganisorAndLoginRequiredMixin,CreateView):
     template_name="leads/lead_create.html"
     form_class=LeadModelForm
     success_url='/leads'
     def form_valid(self,form):
         #todo send email
         send_mail(
             subject="a lead has been created",message="go to the site to see the new lead",
             from_email="test@test.com",
             recipient_list=["test2@test.com"]
         )
         return super(LeadCreateView,self).form_valid(form)

def lead_create(request):
   form=LeadModelForm()
   if request.method=="POST":
       
       form=LeadModelForm(request.POST)
       if form.is_valid():
          form.save()
          return redirect("/leads")
   context={
      "form":form
   }
   return render(request,"leads/lead_create.html",context)



class  LeadUpdateView(OrganisorAndLoginRequiredMixin,UpdateView):
     template_name="leads/lead_update.html"
     form_class=LeadModelForm
     success_url='/leads'
     def get_queryset(self):
         user=self.request.user
         return Lead.objects.filter(organisation=user.userprofile)

def  lead_update(request ,pk):
   lead=Lead.objects.get(id=pk)
   form=LeadModelForm(instance=lead)
   if request.method=="POST":
       form=LeadModelForm(request.POST ,instance=lead)
       if form.is_valid():
          form.save()
          return redirect("/leads")
   context={
    "form":form,
    "lead":lead
   }
   return render(request,"leads/lead_update.html",context)


class  LeadDeleteView(OrganisorAndLoginRequiredMixin,DeleteView):
     template_name="leads/lead_delete.html"
     success_url='/leads'
     def get_queryset(self):
         user=self.request.user
         return Lead.objects.filter(organisation=user.userprofile)
def lead_delete(request,pk):
   lead=Lead.objects.get(id=pk)
   lead.delete()
   return redirect("/leads")

# def lead_update(request,pk):
#    lead=Lead.objects.get(id=pk)
#    form=LeadForm()
#    if request.method=="POST":
       
#        form=LeadForm(request.POST)
#        if form.is_valid():
#          first_name=form.cleaned_data['first_name']
#          last_name=form.cleaned_data['last_name']
#          age=form.cleaned_data['age']

#          lead.first_name=first_name
#          lead.last_name=last_name
#          lead.age=age
#          lead.save()
#          return redirect("/leads")
   # context={
   #  "form":form,
   #  "lead":lead
   # }
   # return render(request,"leads/lead_update.html",context)

# def lead_create(request):
   # form=LeadForm()
   # if request.method=="POST":
   #     print("recieving data")
   #     form=LeadForm(request.POST)
   #     if form.is_valid():
   #        first_name=form.cleaned_data['first_name']
   #        last_name=form.cleaned_data['last_name']
   #        age=form.cleaned_data['age']
   #        agent=Agent.objects.first()
   #        Lead.objects.create(
   #           first_name=first_name,
   #           last_name=last_name,
   #           age=age,
   #           agent=agent
   #        )
         
   #        return redirect("/leads")
#    context={
#       "form":form
#    }
#    return render(request,"leads/lead_create.html",context)