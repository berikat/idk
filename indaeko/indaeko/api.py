import frappe
from frappe.utils.response import build_response
from frappe import _

@frappe.whitelist()
def get_indaeko_invoice(from_date=None, to_date=None, limit_start=None, limit_page_length=None):
    if not limit_page_length:
        limit_page_length = 20
    if not limit_start:
        limit_start = 0 
    datalist = frappe.db.sql("""SELECT 
concat(a.`name`,'-',b.`name`) id
, a.`name` invoice_number
, a.company
, a.posting_date invoice_date
, a.title account_name
, c.`code` account_code
, b.item_code
, b.item_name
, b.qty
, b.uom
, b.rate unit_price
, b.amount
, a.currency
, b.total_weight net_weight
, a.modified
, a.remark_sales_invoice
FROM `tabSales Invoice` a
JOIN `tabSales Invoice Item` b ON a.`name` = b.`parent` AND b.`parenttype` = 'Sales Invoice'
JOIN `tabCustomer` c ON a.title = c.`name`
WHERE a.docstatus != 2 and a.modified >= %s and a.modified < %s
limit %s,%s""", (from_date, to_date, int(limit_start), int(limit_page_length)), as_dict=True)
    return get_response(datalist)

def get_response(datalist):
    frappe.local.response.update({
        "data":  datalist})
    return build_response("json")