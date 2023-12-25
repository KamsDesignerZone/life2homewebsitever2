import frappe

def get_context(context):

    context.current_year = "2003"

    print (context.faqs)

    return context