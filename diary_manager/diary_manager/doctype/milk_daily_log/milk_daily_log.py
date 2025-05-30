# Copyright (c) 2024, nani-samireddy and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MilkDailyLog(Document):
	def before_save(self):
		# Set the total milk values before saving
		self.set_total_milk()

	def on_update(self):
		frappe.log_error("After Save Triggered for Milk Daily Log")
		# Get all the animal tags from the milk_log_table table
		animal_tags = [log_entry.animal_tag for log_entry in self.milk_log_table if log_entry.animal_tag]
		# Update the total milk produced for each animal
		for animal_tag in animal_tags:
			self.update_animal_total_milk_produced(animal_tag)

	def update_animal_total_milk_produced(self, animal_tag):
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


	def set_total_milk(self):
		# Calculate total milk for cows and buffaloes
		total_cow_milk = 0
		total_buffalo_milk = 0
		for log_entry in self.milk_log_table:
			if log_entry.animal_type == "Cow":
				total_cow_milk += log_entry.mpm + log_entry.mpe
			elif log_entry.animal_type == "Buffalo":
				total_buffalo_milk += log_entry.mpm + log_entry.mpe
		## Set the total milk values
		self.total_cow_milk = total_cow_milk
		self.total_buffalo_milk = total_buffalo_milk

