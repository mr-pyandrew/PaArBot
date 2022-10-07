import pytz
from django.utils import timezone

TOKEN = '1802295789:AAGvG723mo6zGzu7VBxRtyRm9t13QF5AumM'

user_timezone = pytz.timezone('Europe/Kiev')

hour = 0

minute = 0

timer = 0

m_post = ''

last_message = ''

admins = [286077227, 811750760]

def time():
    time_ = timezone.now().astimezone(user_timezone)
    return time_


hello_message = ''