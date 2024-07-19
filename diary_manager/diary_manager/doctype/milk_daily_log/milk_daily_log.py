# Copyright (c) 2024, nani-samireddy and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class MilkDailyLog(Document):
	def before_save(self):
		# Set the total milk values before saving
		self.set_total_milk()

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

