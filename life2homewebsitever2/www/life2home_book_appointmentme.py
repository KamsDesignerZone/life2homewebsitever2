import frappe

def get_context(context):
    context.message_on_appointment_page_for_me = frappe.db.get_single_value("Registration Message Configuration", "message_on_appointment_page_for_me")
    return context