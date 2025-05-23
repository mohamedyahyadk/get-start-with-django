from django.views import generic
from django.core.mail import send_mail 
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.urls import reverse_lazy
from agents.forms import AgentModelForm
from .mixins import OrganisorAndLoginRequiredMixin 
# Create your views here.

class AgentListView(OrganisorAndLoginRequiredMixin,generic.ListView):
    template_name='agents/agent_list.html'
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)



class AgentCreateView(OrganisorAndLoginRequiredMixin,generic.CreateView):
      template_name="agents/agent_create.html"
      form_class=AgentModelForm
      success_url=reverse_lazy("agents:agent-list")

      def form_valid(self, form):
           user= form.save(commit=False)
           user.is_agent=True
           user.is_organisor=False
           user.set_password(f"{random.randint(0,1000000)}")
           user.save()
           Agent.objects.create(
               user=user,
               organisation=self.request.user.userprofile
           )
           send_mail(
               subject=" you are invited to be an agent",
               message="you were added as an agent on dgjcrm .please come loginto start working",
               from_email="admin@test.com",
               recipient_list=[user.email]
           )
           return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(OrganisorAndLoginRequiredMixin,generic.DetailView):
      template_name="agents/agent_detail.html"
      context_object_name="agent"
      def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(OrganisorAndLoginRequiredMixin,generic.UpdateView):
      template_name="agents/agent_update.html"
      form_class=AgentModelForm
      success_url=reverse_lazy("agents:agent-list")
      def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
      

class AgentDeleteView(OrganisorAndLoginRequiredMixin,generic.DeleteView):
      template_name="agents/agent_delete.html"
      success_url=reverse_lazy("agents:agent-list")
      def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

      