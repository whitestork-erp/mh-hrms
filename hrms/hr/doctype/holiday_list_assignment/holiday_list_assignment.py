# Copyright (c) 2025, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_link_to_form, getdate

from hrms.payroll.doctype.salary_structure_assignment.salary_structure_assignment import DuplicateAssignment


class HolidayListAssignment(Document):
	def validate(self):
		self.validate_assignment_start_date()
		self.validate_exisiting_assignment()

	def validate_exisiting_assignment(self):
		holiday_list = frappe.db.exists(
			"Holiday List Assignment",
			{"assigned_to": self.assigned_to, "from_date": self.from_date, "docstatus": 1},
		)

		if holiday_list:
			frappe.throw(
				_("Holiday List Assignment for {0} already exists: {1}").format(
					self.assigned_to, get_link_to_form("Holiday List Assignment", holiday_list)
				),
				DuplicateAssignment,
			)

	def validate_assignment_start_date(self):
		holiday_list_start, holiday_list_end = frappe.db.get_value(
			"Holiday List", self.holiday_list, ["from_date", "to_date"]
		)
		assignment_start_date = getdate(self.from_date)
		if (assignment_start_date < holiday_list_start) or (assignment_start_date > holiday_list_end):
			frappe.throw(_("Assignment start date cannot be ouside holiday list dates"))
