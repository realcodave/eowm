from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate

# Create your views here.


# class SignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     # success_url = reverse_lazy('login')
    # template_name = 'signup.html'

    # def form_valid(self, form):
    #     # This method is called when valid form data has been POSTed.
    #     # It should return an HttpResponse.
        
    #     form.send_email()
    
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = request.POST["email"]
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            subject = 'welcome to Edith Okubanjo World Ministry'
            message = f'Hi {user.username}, Welcome To Edith Okunbanjo World Ministry \n You"re all set, You can Listen to Rev. Edith Okubanjo here, Register for the Ark Of God Theological School, book halls and rooms, Thank you and God Grace Rest Upon All You Do.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail( subject, message, email_from, recipient_list )

            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
   


