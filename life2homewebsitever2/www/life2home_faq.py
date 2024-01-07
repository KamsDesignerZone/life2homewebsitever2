import frappe

def get_context(context):

    context.faqs = frappe.db.get_list('FAQ', order_by="sequence asc", fields=['question', 'answer'], ignore_permissions=True)

    return context