# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate


class HolidayListAssignment(Document):
	def validate(self):
		self.validate_overlap_with_exisiting_assigment()
		self.set_dates()

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
		if relieving_date and getdate(self.to_date) > relieving_date:
			self.to_date = relieving_date
