import datetime
import json

import frappe
import pytz
from frappe import _

from frappe.utils.file_manager import upload

def get_context(context):
    context.message_on_appointment_page_for_me = frappe.db.get_single_value("Registration Message Configuration", "message_on_appointment_page_for_me")
    return context

# For This To Work Make Sure Guest User Has Create Permission On File DocType. Check Via Role List , Go To : Role List=>Select Role=>Confirm if File Doctype is Listed
@frappe.whitelist(allow_guest=True)
def uploadfile():
	ret = None
	try:
		if frappe.form_dict.get("from_form"):
			try:
				ret = frappe.get_doc(
					{
						"doctype": "File",
						"attached_to_name": frappe.form_dict.docname,
						"attached_to_doctype": frappe.form_dict.doctype,
						"attached_to_field": frappe.form_dict.docfield,
						"file_url": frappe.form_dict.file_url,
						"file_name": frappe.form_dict.filename,
						"is_private": frappe.utils.cint(frappe.form_dict.is_private),
						"content": frappe.form_dict.filedata,
						"decode": True,
					}
				)
				ret.save()
			except frappe.DuplicateEntryError:
				# ignore pass
				ret = None
				frappe.db.rollback()
		else:
			if frappe.form_dict.get("method"):
				method = frappe.get_attr(frappe.form_dict.method)
				ret = method()
	except Exception:
		frappe.errprint(frappe.utils.get_traceback())
		frappe.response["http_status_code"] = 500
		ret = None

	return ret

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

	appointment.custom_booked_by = "Marketing Executive"

	appointment.status = "Open"
	appointment.insert(ignore_permissions=True)
	return appointment

def convert_to_system_timezone(guest_tz, datetimeobject):
	guest_tz = pytz.timezone(guest_tz)
	datetimeobject = guest_tz.localize(datetimeobject)
	system_tz = pytz.timezone(frappe.utils.get_time_zone())
	datetimeobject = datetimeobject.astimezone(system_tz)
	return datetimeobject