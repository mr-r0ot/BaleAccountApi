# چیست و چرا؟
کتابخانه های زیادی برای اتصال و ساخت ربات بله که به آن بازوی بله هم می گویند وجود دارد.
اما تا کنون هیچ کتابخانه رو ندیدم که امکان کنترل خود اکانت رو فراهم بکنه و بله هم مستندات در این باره منتشر نکرده.
برای یه پروژه به کنترل حساب بله نیاز پیدا کردم پس این کتابخانه رو ساختم
در مراحل آزمایشی هست و گسترده و پشتیبانی از تمام امکانات رو نداره چون در حد نیازه پروژه خودم نوشته شده

اگر کسی مایل بود می تونه درخواست های توسعه رو به گیت هاب بفرسته و د گسترش این کتابخانه کمک کنه

https://github.com/mr-r0ot/BaleAccountApi


# مستندات
### نصب
```
pip install BaleAccountApi
```
### استفاده
```
#افزودن
import BaleAccountApi


# ساخت یک سشن جدید
home = BaleAccountApi.start()

# ارسال یه کد تایید(سشن همواره باید به تابع ها پاس داده شود)
if BaleAccountApi.send_otp_code(home, "09123456789"):
    print("با موفقیت ارسال شد")
else:
    print("خطا")


# گرفتن کد تایید و ورود به حساب
while True:
    code = input("Enter code: ")
    if BaleAccountApi.login(home, code):
        print("خوش اومدی :)")
        break
    else:
        print("کد اشتباه بود")

# در بله دو نوع id وجود دارد:
# یکی به صورت متنی و رشته است و یکی آیدی ععدی
# برای استفاده در این کتابخانه نیاز به آیدی عددی داریم پس با این تابع می توانیم:
# تبدیل آیدی رشته   به    آیدی ععدی قابل استفاده
ID='EnterYourBaleStringID' 
chat_uid = BaleAccountApi.convert_id_to_uid(home, ID)
print(f' Caht UID : {chat_uid}')



# باز کردن یه چت با آیدی عددی
# می تواند گروه کانال پیوی و... باشد
BaleAccountApi.open_chat(home, chat_uid=chat_uid)

# مثال خواندن پیام ها
out = BaleAccountApi.readmessages(home)
print(out)

# مثال ارسال پیام
if BaleAccountApi.send_message(home, 'HIII :) '):
    print("Sended :)")
else:
    print('My bad :(')

```
