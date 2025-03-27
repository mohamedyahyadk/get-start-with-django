from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent
from django.urls import reverse_lazy
from agents.forms import AgentModelForm
# Create your views here.

class AgentListView(LoginRequiredMixin,generic.ListView):
    template_name='agents/agent_list.html'
    def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)



class AgentCreateView(LoginRequiredMixin,generic.CreateView):
      template_name="agents/agent_create.html"
      form_class=AgentModelForm
      success_url=reverse_lazy("agents:agent-list")

      def form_valid(self, form):
           agent= form.save(commit=False)
           agent.organisation=self.request.user.userprofile
           agent.save()
           return super(AgentCreateView,self).form_valid(form)

class AgentDetailView(LoginRequiredMixin,generic.DetailView):
      template_name="agents/agent_detail.html"
      context_object_name="agent"
      def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)


class AgentUpdateView(LoginRequiredMixin,generic.UpdateView):
      template_name="agents/agent_update.html"
      form_class=AgentModelForm
      success_url=reverse_lazy("agents:agent-list")
      def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)
      

class AgentDeleteView(LoginRequiredMixin,generic.DeleteView):
      template_name="agents/agent_delete.html"
      success_url=reverse_lazy("agents:agent-list")
      def get_queryset(self):
        organisation=self.request.user.userprofile
        return Agent.objects.filter(organisation=organisation)

      