import frappe
from frappe import _
from datetime import datetime
from datetime import timedelta

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