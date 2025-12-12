import frappe


def execute():
	old_workspaces = [
		"Expense Claims",
		"Salary Payout",
		"Employee Lifecycle",
		"Overview",
		"Shift & Attendance",
	]

	for workspace in old_workspaces:
		if frappe.db.exists("Workspace", {"name": workspace, "public": 1, "for_user": ""}):
			frappe.delete_doc("Workspace", workspace, force=True)
