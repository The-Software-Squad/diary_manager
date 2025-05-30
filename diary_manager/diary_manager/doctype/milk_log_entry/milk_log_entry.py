# Copyright (c) 2024, nani-samireddy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class MilkLogEntry(Document):
	def validate(self):
		frappe.log_error("Before Save Triggered for Milk Log Entry")

	def after_save(self):
		self.update_total_milk_produced()

	# def on_trash(self):
	# 	self.update_total_milk_produced()

	def update_total_milk_produced(self):
		if not self.animal_tag:
			return

		# Fetch all Milk Log Entries for this animal (excluding trashed)
		milk_logs = frappe.get_all(
			"Milk Log Entry",
			filters={"animal_tag": self.animal_tag},
			fields=["mpm", "mpe"]
		)

		# Calculate total milk produced (mpm + mpe)
		total = sum((entry["mpm"] or 0) + (entry["mpe"] or 0) for entry in milk_logs)

		# Update the Animal document's total
		frappe.db.set_value("Animal", self.animal_tag, "animal_milk_produced", total)
