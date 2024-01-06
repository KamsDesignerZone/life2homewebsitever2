import datetime
import json

import frappe
import pytz
from frappe import _

def get_context(context):
    context.new_booking_message = frappe.db.get_single_value("Registration Message Configuration", "message_on_appointment_page")
    context.site_types = frappe.db.get_list('Site Type', fields=['site_type_name'], order_by="sequence asc")
    context.site_cobfigurations = frappe.db.get_list('Site Configuration', fields=['site_configuration_name'], order_by="sequence asc")
    context.project_completion_priorities = frappe.db.get_list('Project Completion Priority', fields=['project_completion_priority_name'], order_by="sequence asc")
    return context

@frappe.whitelist(allow_guest=True)
def create_appointment(date, time, tz, contact):
	format_string = "%Y-%m-%d %H:%M:%S"
	scheduled_time = datetime.datetime.strptime(date + " " + time, format_string)
	# Strip tzinfo from datetime objects since it's handled by the doctype
	scheduled_time = scheduled_time.replace(tzinfo=None)
	scheduled_time = convert_to_system_timezone(tz, scheduled_time)
	scheduled_time = scheduled_time.replace(tzinfo=None)
	# Create a appointment document from form
	appointment = frappe.new_doc("Appointment")
	appointment.scheduled_time = scheduled_time
	contact = json.loads(contact)
	appointment.customer_name = contact.get("name", None)
	appointment.customer_phone_number = contact.get("customer_phone_number", None)
	appointment.customer_email = contact.get("email", None)

	appointment.custom_site_type = contact.get("site_type", None)
	appointment.custom_site_configuration = contact.get("site_configuration", None)
	appointment.custom_site_locality = contact.get("site_locality", None)
	appointment.custom_site_full_address = contact.get("site_fulladdress", None)
	appointment.custom_project_completion_priority = contact.get("project_completion_priority", None)
	appointment.custom_booked_by = "Client"

	appointment.status = "Open"
	appointment.insert(ignore_permissions=True)
	return appointment

def convert_to_system_timezone(guest_tz, datetimeobject):
	guest_tz = pytz.timezone(guest_tz)
	datetimeobject = guest_tz.localize(datetimeobject)
	system_tz = pytz.timezone(frappe.utils.get_time_zone())
	datetimeobject = datetimeobject.astimezone(system_tz)
	return datetimeobject