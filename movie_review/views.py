import hashlib
import string
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import random

from movie_review.models import *
from movie_review.utils import *

# Create your views here.

def registration_page(request):
    return render(request,"registration_page.html")

def add_user(request):
    name=request.POST['name']
    email=request.POST['email']
    photo=request.FILES['photo']
    password=request.POST['password']

    salt=''.join(random.choices(string.ascii_letters,k=7))
    password=salt+password

    password=hashlib.md5(password.encode('utf-8')).hexdigest()
    if Users.objects.filter(email=email).exists():
        return HttpResponse('''<script>alert("An account with the provided email already exists");window.location="/login_page/"</script> ''')

    login=Login()
    login.email=email
    login.password=password
    login.type,login.salt="user",salt
    login.save()

    user=Users()
    user.name,user.email,user.photo,user.password=name,email,photo,password
    user.login_id=login.id
    user.save()
    return HttpResponse('''<script>alert("sign up successfully");window.location="/login_page/"</script> ''')
    
def login_page(request):
    return render(request,"login_page.html")

def login(request):
    email=request.POST['email']
    password=request.POST['password']
    user=Login.objects.filter(email=email).first()
    if user:
        salt=user.salt
        password=salt+password
        password=hashlib.md5(password.encode('utf-8')).hexdigest()
        try:  
          login=Login.objects.get(email=email,password=password)
        
        
          if login:
            user_id=Users.objects.get(email=email).id
            request.session['lid']=user_id
            print(login.email)
            if login.type=="admin":
                request.session['type']=login.type
                return HttpResponse('''<script>alert("Login successfully");window.location.replace"/add_movie_page/"</script>''')
            else:
                request.session['type']=login.type
                return HttpResponse('''<script>alert("Login successfully");window.location.replace("/home_page/")</script>''')  
          else:
               return HttpResponse('''<script>alert("invalid password. Please try again");window.location="/login_page/"</script>''')     
        except:
            return HttpResponse('''<script>alert("invalid password. Please try again");window.location="/login_page/"</script>''')
    else:
        return HttpResponse(''' <script>alert("Invalid email or user not exist.Please try again");window.location="/login_page/"</script>''')    
    
def add_movies_page(request):
    if check_admin_authentication(request):
        return render(request,"add_movie_page.html")
    else:
        return HttpResponse('''<script>alert("you are not admin ,admin can only add movie");window.location="/home_page/"</script>''')


def add_movie(request):
    name=request.POST['name']
    photo=request.FILES['photo']
    language=request.POST['language']
    release_date=request.POST['release_date']
    actors=request.POST['actors']
    director=request.POST['director']
    writer=request.POST['writer']
    discription=request.POST['discription']
    categories_tags = request.POST['categories_tags']
    movie=Movies()

    movie.name=name
    movie.photo=photo
    movie.language=language
    movie.release_date=release_date
    movie.actors=actors
    movie.director=director
    movie.writer=writer
    movie.discription=discription
    movie.categories_tags=categories_tags

    movie.save()
    return HttpResponse(''' <script>alert("movie added successfully");window.location="/add_movie_page/"</script>''')
    
def movie_details_page(request,id):
    movie=Movies.objects.get(id=id)
    likes=Likes.objects.filter(movie_id=id)
    dislike=Dislikes.objects.filter(movie_id=id)
    rating=get_avg_rating(id)
    tags=movie.categories_tags.split(",")
    movie.categories_tags=tags
    reviews=Reviews.objects.filter(movie_id=id)
    print(movie.photo)
    if check_user_authenticated(request):
        user_id=request.session['lid']
        is_saved=check_is_saved(user_id,id)
    else:
        is_saved=False    

    return render(request,"movie_details_page.html",{"movie":movie,"likes":likes.count(),"dislikes":dislike.count(),"rating":rating,"reviews":reviews,"is_saved":is_saved})   

def add_like(request):
    if check_user_authenticated(request):
      id=request.POST['id']
      user_id=request.session['lid']

      if check_is_liked(user_id,id):

        return JsonResponse({"status_code":202,"message":"movie already liked",})
      
      else:

        if check_is_disliked(user_id,id):

            remove_dislike_in_database(user_id,id)

        add_like_in_database(user_id,id)
        like=Likes.objects.filter(movie_id=id)
        dislike=Dislikes.objects.filter(movie_id=id)
        return JsonResponse({"status_code":201,"message":"movie liked successfully","likes":like.count(),"dislikes":dislike.count()})
    else:
        return JsonResponse({"status_code":401,"message":"please login",})  
   

def add_dislike(request):
   if check_user_authenticated(request): 
    movie_id=request.POST['id']
    user_id=request.session['lid']

    if check_is_disliked(user_id,movie_id):
        return JsonResponse({"status_code":202,"message":"movie already disliked",})
    else:
        if check_is_liked(user_id,movie_id):
            remove_like_in_database(user_id,movie_id)
        add_dislike_in_database(user_id,movie_id)    
        dislike=Dislikes.objects.filter(movie_id=movie_id)
        like=Likes.objects.filter(movie_id=movie_id)
        return JsonResponse({"status_code":201,"message":"movie disliked successfully","dislikes":dislike.count(),"likes":like.count()})
   else:
        return JsonResponse({"status_code":401,"message":"please login",})

def add_rating(request):
   if check_user_authenticated(request): 
      movie_id=request.POST['id']
      rate=request.POST['rating']
      user_id=request.session['lid']
      if check_is_rated(user_id,movie_id):
        update_rating(user_id,movie_id,rate)
      else:
        add_rating_in_database(user_id,movie_id,rate)   
      avg_rate=get_avg_rating(movie_id)
      print(avg_rate)
      return JsonResponse({"status_code":201,"message":"movie rating added successfully","rating":avg_rate})
   else:
        return JsonResponse({"status_code":401,"message":"please login",})
   
   

def add_review(request,id):
   if check_user_authenticated(request): 
    user_id=request.session['lid']
    reviewText=request.POST['review']
    review=Reviews()
    review.movie_id=id
    review.review=reviewText
    review.user_id=user_id
    review.save()
    return HttpResponse(f'''<script>alert("review added successfully");window.location="/movie_details_page/{id}/"</script>''')
   else:
        return JsonResponse({"status_code":401,"message":"please login",})
   
def view_liked_movies_page(request):
    if check_user_authenticated(request):
        user_id=request.session['lid']
        print(user_id)
        likes=Likes.objects.filter(user_id=user_id)
        movies = [Movies.objects.get(id=like.movie_id) for like in likes]
        return render(request,"view_liked_movie_page.html",{"movies":movies})  
    else:
        return HttpResponse('''<script>alert("please login");window.location="/login_page/"</script>''')
   

def view_movies_page(request):
    movies=Movies.objects.all()
    return render(request,"view_movies_page.html",{"movies":movies})  

def delete_movie(request,id):
    movie=Movies.objects.get(id=id)
    movie.delete()
    return HttpResponse(''' <script>alert("movie delete successfully");window.location="/view_movies_page/"</script>''')

def home_page(request):
    if check_user_authenticated(request):
         user_id=request.session['lid']
         likes=Likes.objects.filter(user_id=user_id)
         liked_movie=[like.movie for like in likes]
         recomanded=Movies.objects.all()[:6]
         slider_photo=[movie.photo for movie in recomanded]

         latest=Movies.objects.all().order_by('-release_date')[:6]
         old_searches=Search.objects.filter(user_id=user_id)[0:2]
         if old_searches:
             old_searches=[search.search for search in old_searches]
         else:
             old_searches=[movie.name for movie in latest]
         return render(request,"home_page.html",{"liked":liked_movie,"recomanded":recomanded,"slider_photo":slider_photo,"latest":latest,"old_searches":old_searches})
    else:
         return JsonResponse({"status_code":401,"message":"please login",})


def search_movie(request):
    
    input=request.POST['search']
    movies=Movies.objects.filter(name__istartswith=input)
    results = [
            {
                'id': movie.id,
                'name': movie.name,
                'image': movie.photo.url # Ensure 'photo' is an ImageField or has a valid URL
            }
            for movie in movies
        ]

    return JsonResponse({"results":results})

def view_search_result_page(request,search):
    if check_user_authenticated:
        user_id=request.session['lid']
        add_search(user_id,search)
        movies=Movies.objects.filter(name__istartswith=search)[0:6]
        movie_with_search_tage=Movies.objects.filter(categories_tags__istartswith=search)
        return render(request,"view_search_result_page.html",{"movies":movies,"search":search,"movie_with_search_tage":movie_with_search_tage})

    else:
        return JsonResponse({"status_code":401,"message":"please login",})     
   
def add_or_remove_save(request):
    if check_user_authenticated:
        user_id=request.session['lid']
        movie_id=request.POST['movie_id']
        if check_is_saved(user_id,movie_id):
            remove_saved(user_id,movie_id)
            message="movie unsaved"
        else:
            save_movie(user_id,movie_id)
            message="movie saved"
        return JsonResponse({"status_code":201,"message":message})
    else:
        return JsonResponse({"status_code":401,"message":"please login"}) 

def check_json_response(request):
    return JsonResponse({"message":"hello"})       


def view_user_profile_page(request,id):
    user=Users.objects.get(id=id)

    likes=Likes.objects.filter(user_id=id)
    liked_movie=[like.movie for like in likes]
    rated=Rating.objects.filter(user_id=id)
    
    reviewed=Reviews.objects.filter(user_id=id).order_by('-time')[0:5]

    return render(request,"view_user_profile_page.html",{"liked":liked_movie,"rated":rated,"user":user,"reviewed":reviewed})

def view_user_rated_movie_page(request,id):
    rated=Rating.objects.filter(user_id=id)
    return render(request,"view_user_rated_movie_page.html",{"rated":rated})

def view_user_liked_movie(request,id):
    liked=Likes.objects.filter(user_id=id)
    movies=[like.movie for like in liked]
    return render(request,"view_liked_movie_page.html",{"movies":movies})

def view_latest_movie_page(request):
    latest=Movies.objects.all().order_by('-release_date')
    return render(request,"view_latest_movie_page.html",{"movies":latest})

def view_profile_page(request):
    if check_user_authenticated(request):
        id=request.session['lid']
        user=Users.objects.get(id=id)
        likes=Likes.objects.filter(user_id=id)
        liked_movie=[like.movie for like in likes]
        rated=Rating.objects.filter(user_id=id)
        reviewed=Reviews.objects.filter(user_id=id).order_by('-time')[0:5]
        return render(request,"view_profile_page.html",{"liked":liked_movie,"rated":rated,"user":user,"reviewed":reviewed})
    else:
        return HttpResponse('''<script>alert("please login");window.location="/login_page/"</script>''')


def logout(request):
    request.session.clear()
    return HttpResponse('''<script>alert("logout successfully ");window.location="/login_page/"</script>''')

def forget_password(request):
    if check_user_authenticated:
        user_id=request.session['lid']
        token=get_random_string(10)
        secret=get_random_string(8)
        already=ForgotPassword.objects.filter(user_id=user_id)
        if already:
            already.delete()
        add_data_on_forgetPasswordDb(user_id,token,secret)
        user=Users.objects.get(id=user_id)
        send_mail(user.email,f"http://127.0.0.1:8000/change_password_page/{user_id}/{token}/")
        request.session.clear()
        return HttpResponse("we will send email to you use it")
    else:
     return HttpResponse('''<script>alert("please login");window.location="/login_page/"</script>''')

def change_password_page(request,id,token):
    user_id=id
    forget=ForgotPassword.objects.filter(user_id=user_id)
    if forget:
        dbData=ForgotPassword.objects.get(user_id=user_id)
        if dbData.token==token:
            print(dbData.end_time)
            if check_if_time_is_expired(dbData.end_time):
                print("enter expiring time")
                if dbData.is_used==False:
                     dbData.is_used=True
                     dbData.save()
                     return render(request,"change_password_page.html",{"secret":dbData.secret,"id":user_id})
                else:
                    print("is used is true")
                    raise Http404("page not fount")
            else:
                print("time expired")
                dbData.delete()
                raise Http404("page not found")
        else:
            print('token is not true')
            print(dbData.token)
            raise Http404("page not found")
    else:
        print("not get from this user id")
        raise Http404("page not found")   

def change_password(request,id,secret):
    user_id=id
    password=request.POST['password']
    confirmpassword=request.POST['confirmpassword']
    forget=ForgotPassword.objects.filter(user_id=user_id)
    if forget:
        dbData=ForgotPassword.objects.get(user_id=user_id)
        if check_if_time_is_expired(dbData.end_time):
            if dbData.is_used==True:
                if dbData.secret==secret:
                    if password==confirmpassword:
                        salt=get_random_string(7)
                        password=salt+password
                        password=hashlib.md5(password.encode('utf-8')).hexdigest()
                        user=Users.objects.get(id=user_id)
                        login_id=user.login_id
                        login=Login.objects.get(id=login_id)
                        user.password=password
                        user.save()
                        login.password=password
                        login.salt=salt
                        login.save()
                        forgeted=ForgotPassword.objects.filter(user_id=user_id)
                        forgeted.delete()
                        return HttpResponse('''<script>alert("password change successfully");window.location="/login_page/"</script>''')
                    else:
                        return HttpResponse("password and confirm password is not same")
                else:
                    print("secret is not match")
                    raise Http404("page not found") 
            else:
                print("is used is not true")
                raise Http404("page not found")   
        else:
            print("time is expired")
            raise Http404("page not found")    
    else:
        print("not get from this user id")
        raise Http404("page not found")    


                    

   













