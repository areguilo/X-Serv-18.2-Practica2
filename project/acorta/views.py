from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

# Create your views here.
from .models import Url

form = """<form action="" method = "POST"><input type="text" name='url' value=""><br><input type="submit"value="Enviar"></form>"""

@csrf_exempt

def acorta_urls(request,resource):

    if request.method == "GET":
        urls_added = Url.objects.all()

        if not resource:

            if not urls_added:
                response = "<html>Hi user!<br><br><body>" + form + "</body>There are not URLs</html>"

            else:
                response = form + "All of URLs:<ul>"
                for url in urls_added:
                    response = response + "<li><a href=" + str(url.id)+ ">" + url.long_url + "</a>" 
            response = response + "</ul>"

        elif resource.isdigit():
            try:
                short_url = Url.objects.get(id = int(resource))
                return HttpResponseRedirect(short_url.long_url)
            except Url.DoesNotExist:
                response = "<html><body>Does not exist!<br><br>" \
                +"<a href=http://localhost:8000/ >Return to Main Menu</a>"

        else:
            response = "<html><body>404: Resource Not Found<br><br>" \
                +"<a href=http://localhost:8000/ >Return to Main Menu</a>"	

    elif request.method == "POST":
        url=request.POST['url']
 
        if url == "":
            response = "<html><body>No url introduced <br><br>" \
                +"<a href=http://localhost:8000/ >Return to Main Menu</a>"
            url=response

        elif url.find("http://")==-1 and url.find("https://")==-1:
            url = "https://" + url	
            try:	
                Url.objects.get(long_url=url)
                response="<html><body>" + str(url) + "is already saved! <br><br>" \
                    +"<a href=http://localhost:8000/ >Return to Main Menu</a>"
            except Url.DoesNotExist:
                new_url = Url(long_url=url)
                new_url.save()        
                response="<html><body>Url saved succesfully!<br><br>"				
                response+="<html>Url: <a href="+ url + ">" + url + "</a><br><br>" 
                response+=	"<html>Shortened url: <a href="+ str(new_url.id) \
                    +">"+str(new_url.id)+"</a><br><br>"
                response+=	"<a href=http://localhost:8000/ >Return to Main Menu</a>"

    else:
        return HttpResponseNotFound("<html>Response not found</html>")				
		
    return HttpResponse(response)
