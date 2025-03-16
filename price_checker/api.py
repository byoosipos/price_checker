import frappe
from frappe import _
from frappe.utils import flt, cint


@frappe.whitelist(allow_guest=True, methods=['GET', 'POST'])
def get_item_by_barcode(barcode=None):
    """
    Get item details by barcode
    
    Args:
        barcode (str): The barcode to search for
        
    Returns:
        dict: Item details including name, code, image, price, etc.
    """
    # Always bypass CSRF validation for this API
    frappe.flags.ignore_csrf = True
    
    # Set CORS headers to allow access from any origin
    if hasattr(frappe, 'local') and hasattr(frappe.local, 'response'):
        frappe.local.response.update({
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, X-Frappe-CSRF-Token, Authorization",
            "Access-Control-Allow-Credentials": "true"
        })
    
    # Handle OPTIONS requests (preflight)
    if frappe.request and frappe.request.method == "OPTIONS":
        return {}
    
    # Log the request for debugging
    frappe.logger().info(f"Price Checker API: Received request for barcode: {barcode}")
    
    # Get barcode from either POST data or GET query params
    if not barcode and frappe.request:
        if frappe.request.method == "GET":
            barcode = frappe.form_dict.get('barcode')
        else:
            barcode = frappe.form_dict.get('barcode')
    
    if not barcode:
        frappe.logger().error("Price Checker API: No barcode provided")
        return {"error": "No barcode provided"}
    
    try:
        # First, check if barcode exists in Item Barcode child table
        barcode_records = frappe.get_all(
            "Item Barcode",
            filters={"barcode": barcode},
            fields=["parent as item_code"]
        )
        
        frappe.logger().info(f"Price Checker API: Barcode records: {barcode_records}")
        
        if barcode_records:
            item_code = barcode_records[0].get("item_code")
            frappe.logger().info(f"Price Checker API: Found item code from Item Barcode: {item_code}")
        else:
            # Alternatively, check if any Item has this as item_code directly
            if frappe.db.exists("Item", barcode):
                item_code = barcode
                frappe.logger().info(f"Price Checker API: Using barcode as item code: {item_code}")
            else:
                # No item found with this barcode
                frappe.logger().error(f"Price Checker API: No item found for barcode: {barcode}")
                return {"error": "Item not found"}
        
        # Get item details
        item = frappe.get_doc("Item", item_code)
        
        if not item:
            frappe.logger().error(f"Price Checker API: Could not get item doc for item code: {item_code}")
            return {"error": "Item not found"}
        
        # Get the selling price from Item Price
        price_list_rate = 0
        currency = "USD"
        try:
            selling_price_list = frappe.db.get_single_value('Selling Settings', 'selling_price_list')
            currency = frappe.get_cached_value('Price List', selling_price_list, 'currency')
            
            price_list = frappe.db.get_value("Item Price", 
                {"item_code": item_code, "selling": 1, "price_list": selling_price_list}, 
                ["price_list_rate"], order_by="valid_from desc")
            
            if price_list:
                price_list_rate = flt(price_list)
                frappe.logger().info(f"Price Checker API: Found price {price_list_rate} {currency} for item {item_code}")
            else:
                frappe.logger().warning(f"Price Checker API: No price found for item {item_code}")
        except Exception as e:
            frappe.log_error(f"Error getting price: {str(e)}")
            try:
                currency = frappe.get_cached_value('Global Defaults', 'None', 'default_currency')
            except:
                currency = "USD"
        
        # Prepare image URL if item has an image
        image = item.image if item.image else None
        
        # Build response data
        result = {
            "item_code": item.item_code,
            "item_name": item.item_name,
            "item_group": item.item_group,
            "description": item.description,
            "image": image,
            "price": price_list_rate,
            "currency": currency or "USD"
        }
        
        frappe.logger().info(f"Price Checker API: Returning result: {result}")
        return result
    except Exception as e:
        frappe.log_error(f"Error in price_checker.api.get_item_by_barcode: {str(e)}")
        frappe.logger().error(f"Price Checker API: Exception: {str(e)}")
        return {"error": str(e)}


@frappe.whitelist(allow_guest=True)
def submit_rating():
    """
    Allow guests to submit ratings without authentication
    """
    try:
        # Log the request for debugging
        frappe.logger().debug("Rating submission received")
        
        # Get the rating from POST data
        rating = frappe.form_dict.get('rating')
        reason = frappe.form_dict.get('reason', '')
        
        if not rating:
            return {"error": "Rating is required"}
        
        # Convert to float and validate
        try:
            rating = float(rating)
            if rating < 1 or rating > 5:
                return {"error": "Rating must be between 1 and 5"}
        except ValueError:
            return {"error": "Invalid rating value"}
        
        # Create a new rating document
        doc = frappe.new_doc("Ratings")
        doc.rate_use = rating
        doc.exact_rating = rating  # Store the same value in exact_rating
        doc.feedback_reason = reason
        
        # Submit the document (bypass workflow)
        doc.docstatus = 1
        doc.insert(ignore_permissions=True)
        
        frappe.logger().debug(f"Rating submitted successfully: {rating}, Reason: {reason}")
        return {"success": True, "message": "Rating submitted successfully"}
    
    except Exception as e:
        frappe.logger().error(f"Error in submit_rating: {str(e)}")
        return {"error": str(e)} 