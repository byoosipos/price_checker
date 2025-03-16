import frappe

def before_request():
    """Handle before_request operations"""
    # Set ignore_csrf flag for every request
    if hasattr(frappe, 'flags'):
        frappe.flags.ignore_csrf = True
    
    # Check if the request is related to price checker
    if hasattr(frappe, 'request') and frappe.request:
        request_path = frappe.request.path
        
        # For price checker pages and API calls, bypass authentication and CSRF checks
        if any(x in request_path for x in ['price_check', 'price_checker']):
            # Bypass CSRF protection for all price checker requests
            frappe.flags.ignore_csrf = True
            
            # Allow guest access for these paths
            if hasattr(frappe, 'session'):
                frappe.session.user = 'Guest'
            
            # Set CORS headers to allow access from any origin
            if hasattr(frappe, 'local') and hasattr(frappe.local, 'response'):
                frappe.local.response.update({
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                    "Access-Control-Allow-Headers": "Content-Type, X-Frappe-CSRF-Token, Authorization",
                    "Access-Control-Allow-Credentials": "true"
                })
            
            # For OPTIONS requests (preflight), return immediately
            if frappe.request.method == "OPTIONS":
                return {}
    
    # Also check specifically for the get_item_by_barcode API
    if hasattr(frappe, 'request') and frappe.request and 'get_item_by_barcode' in frappe.request.path:
        frappe.flags.ignore_csrf = True
        if hasattr(frappe, 'session'):
            frappe.session.user = 'Guest' 