import frappe

@frappe.whitelist()
def update_animal_total_milk_produced(animal_tag):
	"""
	Update the total milk produced for a given animal.
	This function fetches all milk log entries for the specified animal
	and calculates the total milk produced.
	"""
	if not animal_tag:
		return

	# Fetch all Milk Log Entries for this animal (excluding trashed)
	milk_logs = frappe.get_all(
		"Milk Log Entry",
		filters={"animal_tag": animal_tag},
		fields=["mpm", "mpe"]
	)

	# Calculate total milk produced (mpm + mpe)
	total = sum((entry["mpm"] or 0) + (entry["mpe"] or 0) for entry in milk_logs)

	# Update the Animal document's total
	frappe.db.set_value("Animal", animal_tag, "animal_milk_produced", total)
