from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(training_enquiry_obj, password, start_date, end_date, is_new_user):
    '''
    Email will be sent when a new user is enrolled in the course.
    '''
    subject = 'Welcome to Our AVIOX!'

    first_name = training_enquiry_obj.first_name
    last_name = training_enquiry_obj.last_name
    course_name = training_enquiry_obj.course.name
    to_email = training_enquiry_obj.email
    from_email = settings.EMAIL_HOST_USER
    login_link = settings.PLATFORM_LOGIN_LINK

    print("first_name : ", first_name)
    print("last_name : ", last_name)
    print("course_name : ", course_name)
    print("to_email : ", to_email)
    print("from_email : ", from_email)
    print("login_link : ", login_link)

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

    html_content = render_to_string('emails/welcome_email.html', context)

    text_content = 'Welcome to our platform!'

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
        print("Email sent successfully.")
    except:
        print("Error in sending email.")



def send_enquiry_email(training_enquiry_obj):
    '''
    Email will be sent when a user makes an enquiry for a course.
    '''

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

    
def send_new_course_email(training_enquiry_obj, start_date, end_date):
    '''
    Email will be sent when an existing user is enrolled in a new course
    '''
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
    '''
    Email will be sent when the user pays the course fees.
    '''
    
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
    '''
    Email will be sent when a user's account is blocked.
    '''

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
    '''
    Email will be sent when a user's account is unblocked.
    '''
    
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


def send_course_extension_email(
            enrollment,
            remark,
            new_end_date
        ):
    '''
    Email will be sent when user extends its course
    '''
    subject = 'Welcome to Our AVIOX!'

    full_name = enrollment.student.first_name + ' ' + enrollment.student.last_name
    course_name = enrollment.course.name
    start_date = str(enrollment.start_date)
    to_email = enrollment.student.email
    from_email = settings.EMAIL_HOST_USER
    login_link = settings.PLATFORM_LOGIN_LINK

    course_ex = enrollment.courseenrollmentextensionlog_set.last()

    if course_ex:
        end_date = str(course_ex.new_end_date)
    else:
        end_date = str(enrollment.end_date)


    context = {
        "full_name" : full_name,
        "course_name" : course_name,
        "start_date" : start_date,
        "end_date" : end_date,
        "to_email" : to_email,
        "from_email" : from_email,
        "login_link" : login_link,
        "remark" : remark,
        "new_end_date" : new_end_date
    }

    html_content = render_to_string('emails/course_extension.html', context)

    text_content = 'Welcome to our platform!'  # fallback for non-HTML email clients

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error in sending email: {e}")
        return False
    