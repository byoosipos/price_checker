import frappe
from frappe import _

def get_context(context):
    """
    Configure context for standalone price check page
    """
    # Force no caching to ensure the page is always up to date
    context.no_cache = 1
    
    # Skip all standard Frappe web layouts
    context.no_sidebar = 1
    context.no_breadcrumbs = 1
    context.no_header = 1
    context.no_footer = 1
    
    # Allow guest access
    if hasattr(frappe.local, 'cookie_manager'):
        frappe.local.cookie_manager.set_cookie("guest_sid", "Guest")
    
    # Set the page to be standalone
    context.standalone = 1
    
    # This page is standalone and shouldn't use the default template
    context.template = "price_checker/www/price_check.html"
    
    # Set additional context variables if needed
    context.hide_login = 1
    context.for_public = 1
    
    return context 