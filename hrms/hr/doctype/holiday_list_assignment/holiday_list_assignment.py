# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form, getdate

from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import DuplicateAssignment


class HolidayListAssignment(Document):
	def validate(self):
		self.set_dates()
		self.validate_from_and_to_dates()
		self.validate_exisiting_assignment()

	def validate_exisiting_assignment(self):
		holiday_list = frappe.db.exists(
			"Holiday List Assignment",
			{"employee": self.employee, "from_date": self.from_date, "docstatus": 1},
		)

		if holiday_list:
			frappe.throw(
				_("Holiday List Assignment for {0} already exists: {1}").format(
					self.employee, get_link_to_form("Holiday List Assignment", holiday_list[0])
				),
				DuplicateAssignment,
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
