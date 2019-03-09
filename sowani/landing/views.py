from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib import messages

from .forms import EmailForm

class HomeView(TemplateView):
    template_name = 'lan.html'

    def get(self, request):
        form = EmailForm()
        return render(request, self.template_name,{'form':form})


    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            mess=messages.success(request, 'Invite Submitted')
            text=form.cleaned_data['email']
            form=EmailForm()
        args={'form':form, 'text':text, 'message':mess}
        return render(request,self.template_name, args)