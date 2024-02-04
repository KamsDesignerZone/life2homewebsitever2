import datetime
import json

import frappe
import pytz
from frappe import _

def get_context(context):
    context.site_types = frappe.db.get_list('Site Type', fields=['site_type_name'], order_by="sequence asc", ignore_permissions=True)
    context.site_cobfigurations = frappe.db.get_list('Site Configuration', fields=['site_configuration_name'], order_by="sequence asc", ignore_permissions=True)
    return context

@frappe.whitelist(allow_guest=True)
def get_quotes(contact):
	contact = json.loads(contact)
	# Step-1 Create a Lead 
	# Step 1.1 Check If Lead With Same Email Id is Present or Not
	# frappe.db.count('Lead', {'email_id': 'hemantsavkar@gmail.com'})
	if frappe.db.count('Lead', {'email_id': contact.get("email", None)},cache=False) == 0:
		quotelead = frappe.new_doc("Lead")
		quotelead.lead_name = contact.get("name", None)
		quotelead.mobile_no = contact.get("customer_phone_number", None)
		quotelead.source = 'Web Site Quote Form'
		quotelead.email_id = contact.get("email", None)
		quotelead.type = 'Client'
		quotelead.possession_received = 'No'
		quotelead.insert(ignore_permissions=True)

	# Step-2 Create an Quotation Request
	quote = frappe.new_doc("Request For Quote")
	quote.name1 = contact.get("name", None)
	quote.mobile = contact.get("customer_phone_number", None)
	quote.email = contact.get("email", None)
	quote.site_type = contact.get("site_type", None)
	quote.site_configuration = contact.get("site_configuration", None)
	quote.insert(ignore_permissions=True)
	return quote