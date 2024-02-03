from . import __version__ as app_version

app_name = "life2homewebsitever2"
app_title = "Life2Home Website Version 2"
app_publisher = "Kams Designer Zone"
app_description = "Life2Home Website Version 2"
app_email = "info@life2home.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/life2homewebsitever2/css/life2homewebsitever2.css"
# app_include_js = "/assets/life2homewebsitever2/js/life2homewebsitever2.js"
app_include_js = "/templates/pages/page.js"

# include js, css files in header of web template
# web_include_css = "/assets/life2homewebsitever2/css/life2homewebsitever2.css"
# web_include_js = "/assets/life2homewebsitever2/js/life2homewebsitever2.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "life2homewebsitever2/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "life2homewebsitever2.utils.jinja_methods",
#	"filters": "life2homewebsitever2.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "life2homewebsitever2.install.before_install"
# after_install = "life2homewebsitever2.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "life2homewebsitever2.uninstall.before_uninstall"
# after_uninstall = "life2homewebsitever2.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "life2homewebsitever2.utils.before_app_install"
# after_app_install = "life2homewebsitever2.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "life2homewebsitever2.utils.before_app_uninstall"
# after_app_uninstall = "life2homewebsitever2.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "life2homewebsitever2.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Appointment": "life2homewebsitever2.www.appointment.appointment.Life2HomeAppointment"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	"cron": {
		"0 7 * * *": [
			"life2homewebsitever2.www.appointment.appointmentjobs.send_reminder_email_for_today"
		],
		"0 7,17 * * *": [
			"life2homewebsitever2.www.appointment.appointmentjobs.send_reminder_email_for_tommorrow"
		]
	}
}

# scheduler_events = {
#	"all": [
#		"life2homewebsitever2.tasks.all"
#	],
#	"daily": [
#		"life2homewebsitever2.tasks.daily"
#	],
#	"hourly": [
#		"life2homewebsitever2.tasks.hourly"
#	],
#	"weekly": [
#		"life2homewebsitever2.tasks.weekly"
#	],
#	"monthly": [
#		"life2homewebsitever2.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "life2homewebsitever2.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "life2homewebsitever2.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "life2homewebsitever2.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["life2homewebsitever2.utils.before_request"]
# after_request = ["life2homewebsitever2.utils.after_request"]

# Job Events
# ----------
# before_job = ["life2homewebsitever2.utils.before_job"]
# after_job = ["life2homewebsitever2.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"life2homewebsitever2.auth.validate"
# ]
website_catch_all = "life2home_404"
fixtures = [
    {
        "dt" :"Service"
    },
    {
        "dt" :"FAQ"
    },
    {
        "dt" :"Contact Information"
    },
    {
        "dt" :"Customer Review"
    },
    {
        "dt" :"Registration Message Configuration"
    },
    {
        "dt" :"Site Type"
    },
    {
        "dt" :"Site Configuration"
    },
    {
        "dt" :"Project Completion Priority"
    },
    {
         "dt": "Custom Field", 
         "filters":[["module", "in", ['Life2Home Website Version 2']]]
    },
    {
        "dt" :"Appointment Booking Settings"
    },
    {
        "dt" :"Lead Source"
    },
    {
        "dt" :"Holiday List"
    },
    {
        "dt" :"SMS Settings"
    },
    {
         "dt": "Custom DocPerm", 
         "filters":[["Role", "in", ['Guest']]]
    }
]