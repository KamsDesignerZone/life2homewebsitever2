import frappe
from frappe import _
from datetime import datetime
from datetime import timedelta
from frappe.core.doctype.sms_settings.sms_settings import send_sms

def send_reminder_email(
                  forDay=1
    ):
    print ("Receiced Value for forDay : {0}".format(forDay))
    pullrecordsforstartdate = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)
    pullrecordsforendtdate = datetime(datetime.now().year, datetime.now().month, datetime.now().day , 23, 59, 59)
    scheduled_date_str = "Today"

    if (forDay==1):
        pullrecordsforstartdate = datetime(datetime.now().year, datetime.now().month, datetime.now().day + 1, 0, 0, 0)
        pullrecordsforendtdate = datetime(datetime.now().year, datetime.now().month, datetime.now().day + 1, 23, 59, 59)
        scheduled_date_str = "Tommorrow"
        
    else:
        pullrecordsforstartdate = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)
        pullrecordsforendtdate = datetime(datetime.now().year, datetime.now().month, datetime.now().day , 23, 59, 59)
        scheduled_date_str = "Today"
        
    print ("Start Pulling Appointment Between {0} to {1}",pullrecordsforstartdate, pullrecordsforendtdate)
    
    all_scheduled_appointments=frappe.db.get_list('Appointment',
                filters=[[
                    'scheduled_time', 'between', [pullrecordsforstartdate, pullrecordsforendtdate]
                ]],
                fields=['customer_name','customer_phone_number', 'customer_email', 'scheduled_time'],
                order_by='customer_name asc',
                page_length=2000
    )
    print (all_scheduled_appointments)

    for scheduled_appointment in all_scheduled_appointments:
        print ("Start Sending Email To {0} on email id {1}".format(scheduled_appointment.customer_name, scheduled_appointment.customer_email))
        template = "life2home_appointment_confirm"
        args = {
                "full_name": scheduled_appointment.customer_name,
                "scheduled_full": scheduled_appointment.scheduled_time.strftime("%d %b %Y %I:%M %p"),
                "scheduled_date": scheduled_date_str,
                "scheduled_time": scheduled_appointment.scheduled_time.strftime("%I:%M %p"),
            }
        frappe.sendmail(
                recipients=[scheduled_appointment.customer_email],
                template=template,
                args=args,
                subject=_("**Appointment Reminder**:{0}".format(scheduled_appointment.scheduled_time.strftime("%d %b %Y %I:%M %p"))),
            )
        # send_sms([scheduled_appointment.customer_phone_number],
        #          "****Reminder***** Hi {0} , Your Appointment With KAMs Designer Zone Is Scheduled For {1} At KAMS Designer Zone Office. --Our Office Address Is-- Arun Park,Shop No. 6,S.No.33/3,Near Aditya Birla Hospital,Dattanagar,Thergaon,Chinchwad, Pune- 411033. --Driving Directions For Office-- https://goo.gl/maps/Ax7Zo4ubWWd45pnL6 Regards, (KAM'S DESIGNER ZONE) For Any Assistance Please Contact 020 71177198 Download Our Mobile App For More Information Android: https://bit.ly/35knTvb iOS: https://apple.co/2WO1Xn7-KAM's Designer Zone".format(
        #               scheduled_appointment.customer_name,
        #               scheduled_date_str)
        #          )
        send_sms([scheduled_appointment.customer_phone_number],
                 "Hi {0}, Your Appointment With Life2Home Interior Products Pvt Ltd Is Scheduled For {1} At Life2Home Interior Products Pvt Ltd Office. Our Office Address Is-- Arun Park, Shop No. 6, S.No.33/3, Near Aditya Birla Hospital, Dattanagar, Thergaon, Chinchwad, Pune- 411033. Regards, LIFE2HOME For Any Assistance Please Contact 7720075070. For More Information visit our website: https://www.life2home.in".format(
                      scheduled_appointment.customer_name,
                      scheduled_date_str)
                 )
        

#life2homewebsitever2.www.appointment.appointmentjobs.send_reminder_email_for_tommorrow                 
def send_reminder_email_for_tommorrow():
    print ('****************** Sending Appointment Reminder For Tommorrow Started ******************')
    send_reminder_email(1)
    print ('****************** Sending Appointment Reminder For Tommorrow Completed ******************')
#life2homewebsitever2.www.appointment.appointmentjobs.send_reminder_email_for_today
def send_reminder_email_for_today():
    print ('****************** Sending Appointment Reminder For Today Started ******************')
    send_reminder_email(0)
    print ('****************** Sending Appointment Reminder For Today Completed ******************')