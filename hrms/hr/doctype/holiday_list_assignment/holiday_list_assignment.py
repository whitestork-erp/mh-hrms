# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class HolidayListAssignment(Document):
	def validate(self):
		self.set_dates()
		self.validate_from_and_to_dates()
		self.validate_overlap_with_exisiting_assigment()

	def validate_overlap_with_exisiting_assigment(self):
		HLA = frappe.qb.DocType("Holiday List Assignment")
		query = (
			frappe.qb.from_(HLA)
			.select(HLA.holiday_list)
			.where((HLA.employee == self.employee) & (HLA.docstatus == 1))
			.where(
				(HLA.from_date.between(self.from_date, self.to_date))
				or (HLA.to_date.between(self.from_date, self.to_date))
				or (HLA.from_date >= self.start_date & HLA.to_date >= self.to_date)
			)
		).run()
		holiday_list = query[0][0] if query else None

		if holiday_list:
			frappe.throw(
				_(
					"{0} already has an existing holiday list assigned for the selected period. Please edit the dates for current or eixsting assignment.\n {1}"
				)
			)

	def set_dates(self):
		joining_date, relieving_date = frappe.db.get_value(
			"Employee", self.employee, ["date_of_joining", "relieving_date"]
		)
		if getdate(self.from_date) < joining_date:
			self.from_date = joining_date
			frappe.msgprint("From date was set to joining date of the employee", alert=True)
		if relieving_date and getdate(self.to_date) > relieving_date:
			self.to_date = relieving_date
			frappe.msgprint("To date was set to relieving date of the employee", alert=True)

	def validate_from_and_to_dates(self):
		if getdate(self.from_date) > getdate(self.to_date):
			frappe.throw(_("From date cannot be less than to date."))

		holiday_list_start, holiday_list_end = frappe.db.get_value(
			"Holiday List", self.holiday_list, ["from_date", "to_date"]
		)
		if getdate(self.from_date) < holiday_list_start:
			frappe.throw(_("Assignment from date cannot be before from date of Holiday list"))
		if getdate(self.to_date) > holiday_list_end:
			frappe.throw(_("Assignment to date cannot be after to date of Holiday list"))
