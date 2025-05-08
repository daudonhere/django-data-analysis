from django.shortcuts import render

# Render home page
def HomePage(request):
    return render(request, "home.html")

# Render error page
def ErrorPage(request, exception=None, status_code=500):
    error_message = str(exception) if exception else "Something went wrong"
    context = {"status_code": status_code, "error_message": error_message}
    return render(request, "error.html", context, status=status_code)
