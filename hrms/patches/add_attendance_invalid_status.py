import frappe

NEW_OPTION = "Invalid"  # your new status

def execute():
    print("Adding new attendance status option...")
    # Get field id safely
    field = frappe.get_all(
        "DocField",
        filters={"parent": "Attendance", "fieldname": "status"},
        fields=["name", "options"],
        limit=1
    )

    if not field:
        frappe.throw("Status field not found in Attendance doctype")

    field = field[0]
    options = (field.get("options") or "").split("\n")

    if NEW_OPTION not in options:
        options.append(NEW_OPTION)
        frappe.db.set_value("DocField", field.name, "options", "\n".join(options))
        frappe.db.commit()
        frappe.clear_cache(doctype="Attendance")
