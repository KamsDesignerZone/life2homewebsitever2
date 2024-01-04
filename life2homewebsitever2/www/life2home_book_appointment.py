import frappe

def get_context(context):
    context.new_booking_message = frappe.db.get_single_value("Registration Message Configuration", "message_on_appointment_page")
    return context