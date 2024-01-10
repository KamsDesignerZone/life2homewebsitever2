from erpnext.crm.doctype.appointment.appointment import Appointment
import frappe
from frappe import _
from datetime import datetime

class Life2HomeAppointment(Appointment):
        def after_insert(self):
            print (" ************ Now Inside Life2HomeAppointment ************ ")
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
            # if frappe.session.user == "Guest":
            #     frappe.msgprint(_("Please check your email to confirm the appointment"))
            # else:
            #     frappe.msgprint(
            #         _("Appointment was created. But no lead was found. Please check the email to confirm")
            #     )
        
        

             
        
             

             