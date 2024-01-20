from erpnext.crm.doctype.appointment.appointment import Appointment
import frappe
from frappe import _
from datetime import datetime

from frappe.core.doctype.sms_settings.sms_settings import send_sms

class Life2HomeAppointment(Appointment):
        def after_insert(self):
            print (" ************ Inside Life2HomeAppointment after_insert ************ ")
            if self.party:
                # Create Calendar event
                self.auto_assign()
                self.create_calendar_event()
            else:
                # Set status to unverified
                self.status = "Unverified"
                # Send email to confirm
            
            self.send_confirmation_email()

        def send_confirmation_email(self):
            verify_url = self._get_verify_url()
            template = "life2home_appointment_confirm"
            print("Current scheduled_time format is {0}".format(type(self.scheduled_time)))
            if(type(self.scheduled_time) == type(template)):
                 self.scheduled_time = datetime.strptime(self.scheduled_time, "%Y-%m-%d %H:%M:%S")
                 print("Current scheduled_time format after upade {0}".format(type(self.scheduled_time)))
            
            args = {
                "link": verify_url,
                "site_url": frappe.utils.get_url(),
                "full_name": self.customer_name,
                "scheduled_full": self.scheduled_time.strftime("%d %b %Y %I:%M %p"),
                "scheduled_date": self.scheduled_time.strftime("%d %b %Y"),
                "scheduled_time": self.scheduled_time.strftime("%I:%M %p"),
            }
            frappe.sendmail(
                recipients=[self.customer_email],
                template=template,
                args=args,
                subject=_("Appointment Confirmation:{0}".format(self.scheduled_time.strftime("%d %b %Y %I:%M %p"))),
            )

            # send_sms(
            #      [self.customer_phone_number],
            #      "****Confirmation***** Hi {0} , Your Appointment With KAMs Designer Zone Requested For {1} , Is Now Acknowledged And Confirmed.Please Visit Our Office On Scheduled Appointment Time --Our Office Address Is-- Arun Park,Shop No. 6,S.No.33/3,Near Aditya Birla Hospital,Dattanagar,Thergaon,Chinchwad, Pune- 411033. --Driving Directions For Office-- https://goo.gl/maps/Ax7Zo4ubWWd45pnL6 Regards, (KAM'S DESIGNER ZONE) For Any Assistance Please Contact 020 71177198 Download Our Mobile App For More Information Android: https://bit.ly/35knTvb iOS: https://apple.co/2WO1Xn7-KAM's Designer Zone".format(
            #           self.customer_name,
            #           self.scheduled_time.strftime("%d %b %Y %I:%M %p")
            #      ),
            # )
            send_sms(
                 [self.customer_phone_number],
                 "Hi {0}, Your Appointment With Life2Home Interior Products Pvt Ltd Requested For {1}, Is Now Acknowledged And Confirmed. Please Visit Our Office On Scheduled Appointment Time. -- Our Office Address Is -- Arun Park, Shop No. 6, S.No.33/3, Near Aditya Birla Hospital, Dattanagar, Thergaon, Chinchwad, Pune- 411033. Regards, LIFE2HOME INTERIOR PRODUCTS PVT LTD For Any Assistance Please Contact 7720075070 For More Information visit our website: https://www.life2home.in/".format(
                      self.customer_name,
                      self.scheduled_time.strftime("%d %b %Y %I:%M %p")
                 ),
            )

            
            # if frappe.session.user == "Guest":
            #     frappe.msgprint(_("Please check your email to confirm the appointment"))
            # else:
            #     frappe.msgprint(
            #         _("Appointment was created. But no lead was found. Please check the email to confirm")
            #     )
        
        

             
        
             

             