app_name = "price_checker"
app_title = "Price Checker"
app_publisher = "byoosicom"
app_description = "Checking Prices"
app_email = "info@byoosi.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "price_checker",
# 		"logo": "/assets/price_checker/logo.png",
# 		"title": "Price Checker",
# 		"route": "/price_checker",
# 		"has_permission": "price_checker.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/price_checker/css/price_checker.css"
# app_include_js = "/assets/price_checker/js/price_checker.js"

# include js, css files in header of web template
# web_include_css = "/assets/price_checker/css/price_checker.css"
# web_include_js = "/assets/price_checker/js/price_checker.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "price_checker/public/scss/website"

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

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "price_checker/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Expose certain routes to the web without login
website_route_rules = [
	{"from_route": "/price_check", "to_route": "price_check"}
]

# Allow guest access to all price checker web pages
allow_guest_to_web_pages = ["price_check"]

# Route to bypass authentication
auth_bypass_routes = ["price_check"]

# Exempt CSRF for price checker API
csrf_exempt = [
    "price_checker.api.get_item_by_barcode",
    "price_checker.api.*"  # Exempt all price checker APIs
]

# Set the home page to the price checker instead of login page
home_page = "price_check"

# Public API endpoints that can be accessed without authentication
public_api_whitelist = [
    "price_checker.api.get_item_by_barcode"
]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "price_checker.utils.jinja_methods",
# 	"filters": "price_checker.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "price_checker.install.before_install"
# after_install = "price_checker.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "price_checker.uninstall.before_uninstall"
# after_uninstall = "price_checker.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "price_checker.utils.before_app_install"
# after_app_install = "price_checker.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "price_checker.utils.before_app_uninstall"
# after_app_uninstall = "price_checker.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "price_checker.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"price_checker.tasks.all"
# 	],
# 	"daily": [
# 		"price_checker.tasks.daily"
# 	],
# 	"hourly": [
# 		"price_checker.tasks.hourly"
# 	],
# 	"weekly": [
# 		"price_checker.tasks.weekly"
# 	],
# 	"monthly": [
# 		"price_checker.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "price_checker.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "price_checker.event.get_events"
# }

# Expose API methods to web without login
allow_guest_access_to_methods = [
	"price_checker.api.get_item_by_barcode",
	"price_checker.api.*",  # Allow all API methods
	"frappe.client.get_value",
	"frappe.client.get",
	"frappe.client.get_list"
]

# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "price_checker.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
before_request = ["price_checker.utils.before_request"]
# after_request = ["price_checker.utils.after_request"]

# Job Events
# ----------
# before_job = ["price_checker.utils.before_job"]
# after_job = ["price_checker.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"price_checker.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

