from django.shortcuts import render

# Create your views here.
def cookies(request):
    """
    Render the cookies page.
    """
    return render(request, 'legal_docs/cookies.html')


def privacy_policy(request):
    """
    Render the privacy policy page.
    """
    return render(request, 'legal_docs/privacy_policy.html')


def terms_and_conditions(request):
    """
    Render the terms and conditions page.
    """
    return render(request, 'legal_docs/terms_and_conditions.html')