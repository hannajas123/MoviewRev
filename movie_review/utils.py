
import smtplib
from email.message import EmailMessage
import random
import string


from movie_review.models import *




def get_movie_like_count(movie_id):
    try:
        likes=Likes.objects.filter(movie_id=movie_id).count()
    except:
        likes=0
    return likes

def get_movie_dislike_count(movie_id):
    try:
        dislikes=Dislikes.objects.filter(movie_id=movie_id).cout()
    except:
        dislikes=0
    return dislikes

def get_avg_rating(movie_id):
        ratings=Rating.objects.filter(movie_id=movie_id)
        count=ratings.count()
        rating=0
        if count!=0:
         for rat in ratings:
           rating+=rat.rate  
         avg=rating/count   
         avg=round(avg,1)
        else:
            avg=0
        return avg    

def check_user_authenticated(request):
    try:
        uid=request.session['lid']
        print(uid)
        if uid:
          authetication=True
        else:
          authetication=False
        return authetication 
    except:
        return False
          

def check_admin_authentication(request):
    try:
        type=request.session['type']
        print(type)
        if type=="admin":
           authetication=True
        else:
           authetication=False
        return authetication  
    except:
        return False

def check_is_liked(user_id,movie_id):
    try:
        like=Likes.objects.get(movie_id=movie_id,user_id=user_id)
        if like:
            is_liked=True
        else:
            is_liked=False
        return is_liked
    except:
        return False

def check_is_disliked(user_id,movie_id):
    try:
        dislike=Dislikes.objects.get(movie_id=movie_id,user_id=user_id)
        if dislike:
            print(True)
            is_disliked=True
        else:
            is_disliked=False
        return is_disliked
    except:
        return False   

def add_like_in_database(user_id,movie_id):
    likes=Likes()
    likes.user_id=user_id
    likes.movie_id=movie_id
    likes.save()

def add_dislike_in_database(user_id,movie_id):
    dislikes=Dislikes()
    dislikes.user_id=user_id
    dislikes.movie_id=movie_id
    dislikes.save()

def remove_like_in_database(user_id,movie_id):
    like=Likes.objects.get(movie_id=movie_id,user_id=user_id)
    like.delete()

def remove_dislike_in_database(user_id,movie_id):
    dislike=Dislikes.objects.get(movie_id=movie_id,user_id=user_id)
    dislike.delete()

def check_is_rated(user_id,movie_id):
    try:
        rate=Rating.objects.get(user_id=user_id,movie_id=movie_id)
        if rate:
            is_rated=True
        else:
            is_rated=False
        return is_rated
    except:
        return False

def update_rating(user_id,movie_id,rate):
    rating=Rating.objects.get(user_id=user_id,movie_id=movie_id)
    rating.rate=rate
    rating.save()               

def add_rating_in_database(user_id,movie_id,rate):
    rating=Rating()
    rating.rate=rate
    rating.movie_id=movie_id
    rating.user_id=user_id
    rating.save()

def add_search(user_id,search):
    searchs=Search()
    searchs.search=search
    searchs.user_id=user_id
    searchs.save()

def check_is_saved(user_id,movie_id):
    try:
        save=Saved.objects.get(user_id=user_id,movie_id=movie_id)
        if save:
            is_saved=True
        else:
            is_saved=False
        return is_saved
    except:
        return False     

def save_movie(user_id,movie_id):
    saved=Saved()
    saved.user_id=user_id
    saved.movie_id=movie_id
    saved.save()

def remove_saved(user_id,movie_id):
    saved=Saved.objects.get(user_id=user_id,movie_id=movie_id)
    saved.delete()




def check_if_time_is_expired(time):
    
    timeNow=timezone.now()
    print("this is time")
    print(timeNow)
    if timeNow < time:
        return True
    else:
        return False

def send_mail(mail,link):
    from_address = "muhammadfoulad8157@gmail.com"
    to_address = mail
    msg = EmailMessage()
    msg['Subject'] = "Reset password"
    msg['From'] = from_address
    msg['To'] = to_address
    msg.set_content(f"Sir,\n\nThis is your password change link: {link}")

    # HTML version with hidden link behind the word "link"
    html_content = f"""
    <html>
      <body>
        <p>Dear user,<br><br>
        Click this <a href="{link}">link</a> to reset your password.<br><br>
        If you didn't request this, you can ignore the email.
        </p>
      </body>
    </html>
    """
    msg.add_alternative(html_content, subtype='html')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
         smtp.ehlo()
         smtp.starttls()
         smtp.login(from_address, "add email password here")
         smtp.send_message(msg)
         
def get_random_string(k):
    random_string=''.join(random.choices(string.ascii_letters,k=k))
    return random_string

def add_data_on_forgetPasswordDb(user_id,token,secret):
      forget_passwordDB=ForgotPassword()
      forget_passwordDB.user_id=user_id
      forget_passwordDB.token=token
      forget_passwordDB.secret=secret
      forget_passwordDB.save() 