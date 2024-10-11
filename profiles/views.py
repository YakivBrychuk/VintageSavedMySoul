from django.shortcuts import render

# Create your views here

def profile(request):
    """ Display the user's profile. """
    template = 'profiles/profile.html'
    context = {
        'on_profile_page': True
    }

    return render(request, template, context)

