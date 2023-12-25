import frappe

def get_context(context):

    context.faqs = frappe.db.get_list('FAQ', order_by="sequence asc", fields=['question', 'answer'],)

    print (context.faqs)

    return context