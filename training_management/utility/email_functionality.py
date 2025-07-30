from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(training_enquiry_obj, password, start_date, end_date, is_new_user):
    print("inside send_welcome_email")
    print("training_enquiry_obj : ", training_enquiry_obj)

    subject = 'Welcome to Our AVIOX!'

    first_name = training_enquiry_obj.first_name
    last_name = training_enquiry_obj.last_name
    course_name = training_enquiry_obj.course.name
    to_email = training_enquiry_obj.email
    from_email = settings.EMAIL_HOST_USER
    login_link = settings.PLATFORM_LOGIN_LINK

    context = {
        'first_name': first_name,
        'last_name': last_name,
        'to_email': to_email,
        'course_name': course_name,
        'from_email': from_email,
        'login_link': login_link,
        'password': password,
        'start_date': start_date,
        'end_date': end_date,
        'is_new_user': is_new_user,
    }
    print('context : ', context)

    html_content = render_to_string('emails/welcome_email.html', context)

    text_content = 'Welcome to our platform!'  # fallback for non-HTML email clients

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
        print("Email sent successfully.")
    except:
        print("Error in sending email.")

    print("DONE")


def send_enquiry_email(training_enquiry_obj):
    print('\n\n\n')
    print("inside Enquiry_email")
    print("training_enquiry_obj : ", training_enquiry_obj)

    subject = 'Welcome to Our AVIOX!'

    first_name = training_enquiry_obj.first_name
    last_name = training_enquiry_obj.last_name
    course_name = training_enquiry_obj.course.name
    to_email = training_enquiry_obj.email
    from_email = settings.EMAIL_HOST_USER

    context = {
        'first_name': first_name,
        'last_name': last_name,
        'to_email': to_email,
        'course_name': course_name,
        'from_email': from_email,
    }
    print('context : ', context)

    html_content = render_to_string('emails/enquiry_email.html', context)

    text_content = 'Welcome to our platform!'  # fallback for non-HTML email clients

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
        print("Email sent successfully.")
    except:
        print("Error in sending email.")

    print("DONE")

    
def send_new_course_email(training_enquiry_obj, start_date, end_date):
    print('\n\n\n')
    print("inside New Assigned Course Email")
    print("training_enquiry_obj : ", training_enquiry_obj)

    subject = 'Welcome to Our AVIOX!'

    first_name = training_enquiry_obj.first_name
    last_name = training_enquiry_obj.last_name
    course_name = training_enquiry_obj.course.name
    to_email = training_enquiry_obj.email
    from_email = settings.EMAIL_HOST_USER
    login_link = settings.PLATFORM_LOGIN_LINK

    context = {
        'first_name': first_name,
        'last_name': last_name,
        'to_email': to_email,
        'course_name': course_name,
        'start_date' : start_date,
        'end_date': end_date,
        'from_email': from_email,
    }
    print('context : ', context)

    html_content = render_to_string('emails/new_course.html', context)

    text_content = 'Welcome to our platform!'  # fallback for non-HTML email clients

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
        print("Email sent successfully.")
    except:
        print("Error in sending email.")
        
    
def send_fee_submit_email(fee_info_obj):
    print('\n\n\n\n')
    print('Inside the fee payment')
    print("Feeinformation Object:", fee_info_obj)
    
    enrollment = fee_info_obj.enrollment
    student = enrollment.student
    course = enrollment.course
    to_email = student.email
    from_email = settings.EMAIL_HOST_USER
    subject = 'Fee Payment confoirmation - Thank You!'
    
    context = {
        'student_name ': enrollment.student,
        'course_name': course.name,
        'amount_paid': fee_info_obj.amount_paid,
        'total_fee': course.total_fee,
        'start_date': enrollment.start_date,
        'end_date': enrollment.end_date,
        'login_link': settings.PLATFORM_LOGIN_LINK,
        
        
    }
    print("Email context:", context)
    
    html_content = render_to_string('emails/fee_submit.html', context)
    text_content  =  "Thank you for your Paymnet."
    
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
        print("Email sent successfully.")
    except:
        print("Error in sending email.")


def send_account_block_email(user_obj):
    print("deactivation email")

    subject = 'Your AVIOX Account Has Been Deactivated'
    to_email = user_obj.email
    from_email = settings.EMAIL_HOST_USER

    context = {
        'first_name': user_obj.first_name,
        'last_name': user_obj.last_name,
    }

    html_content = render_to_string('emails/account_block.html', context)
    text_content = 'Your account has been deactivated. Please contact HR.'

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()
    
    
def send_account_unblock_email(user_obj):
    print("sending activation email")
    
    subject= "Your Aviox Account Has Been Activated"
    to_email = user_obj.email
    from_email = settings.EMAIL_HOST_USER
    
    context = {
        'first_name': user_obj.first_name,
        'last_name':user_obj.last_name,
        'login_link': settings.PLATFORM_LOGIN_LINK 
        }
    
    html_content= render_to_string('emails/account_unblock.html', context)
    text_content= "Your account has been activated. Please check it"
    
    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()
    

def send_custom_email(subject, message, recipient_list, from_email=None):
    if not from_email:
        from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
