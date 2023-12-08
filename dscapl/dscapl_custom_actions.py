from __future__ import unicode_literals
from ast import Pass
from datetime import datetime
import frappe
import json
import re
import copy
import math
import frappe.utils
from frappe import utils
from frappe.utils import cstr, flt, getdate, cint, nowdate, add_days, get_link_to_form
from frappe import _
from six import string_types
from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc
from datetime import datetime, timedelta, date
from frappe.desk import query_report
from erpnext.stock.stock_balance import update_bin_qty, get_reserved_qty
from frappe.desk.notifications import clear_doctype_notifications
from frappe.contacts.doctype.address.address import get_company_address
from erpnext.selling.doctype.customer.customer import check_credit_limit
from erpnext.stock.doctype.item.item import get_item_defaults
from erpnext.accounts.utils import get_fiscal_year, get_balance_on
from erpnext.setup.doctype.item_group.item_group import get_item_group_defaults
from erpnext.accounts.report.accounts_receivable_summary.accounts_receivable_summary import execute as get_ageing
from calendar import monthrange
from datetime import datetime, timedelta
import requests
import logging


# --------------------------------------------------------------------------------------------------------
# This Fuction Update The Price List of Item When submit purchase invoice
@frappe.whitelist()
def update_price_list(doc,event):

	for i in doc.items:
			is_item_exist = frappe.db.exists('Item Price',{'item_code': i.item_code})

			if is_item_exist != None:
				if i.discount_percentage > float('10'):
					price_list_item = frappe.get_doc('Item Price',{'item_code': i.item_code})

					if price_list_item.price_list_rate != i.price_list_rate:
						frappe.set_value('Item Price',{'item_code': i.item_code},'price_list_rate',i.price_list_rate)
						frappe.set_value('Item Price',{'item_code': i.item_code},'valid_from',doc.bill_date)
						frappe.db.commit()
			else:
				if i.brand != 'Legrand':
					new_item_price_list = frappe.new_doc('Item Price')
					new_item_price_list.item_code = i.item_code
					new_item_price_list.item_name = i.item_name
					new_item_price_list.brand = i.brand
					new_item_price_list.item_description = i.description
					new_item_price_list.buying = True
					# new_item_price_list.selling = True
					new_item_price_list.price_list = 'Standard Buying'
					new_item_price_list.price_list_rate = i.price_list_rate
					new_item_price_list.valid_from = doc.bill_date
					new_item_price_list.insert()
# --------------------------------------------------------------------------------------------------------
