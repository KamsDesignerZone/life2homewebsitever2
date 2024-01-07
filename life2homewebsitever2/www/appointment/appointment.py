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
            template = "life2home_confirm_appointment"
            args = {
                "link": verify_url,
                "site_url": frappe.utils.get_url(),
                "full_name": self.customer_name,
                "scheduled_time": datetime.strptime(self.scheduled_time, "%Y-%m-%d %H:%M:%S").strftime("%d %b %Y %I:%M %p"),
            }
            frappe.sendmail(
                recipients=[self.customer_email],
                template=template,
                args=args,
                subject=_("Appointment Confirmation From Life2Home"),
            )
            if frappe.session.user == "Guest":
                frappe.msgprint(_("Please check your email to confirm the appointment"))
            else:
                frappe.msgprint(
                    _("Appointment was created. But no lead was found. Please check the email to confirm")
                )
        