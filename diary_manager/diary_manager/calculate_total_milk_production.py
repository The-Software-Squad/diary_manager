import frappe

@frappe.whitelist()
def calculate_total_milk_production(doc, method):
    # Clear the existing entries in the worker milk production table
    doc.worker_milk_production = []

    # Dictionary to hold the total milk production per worker
    worker_milk_totals = {}

    # Loop through each Milk Log Entry and aggregate the milk production
    for entry in doc.get('milk_log_table'):
        worker = entry.worker_name
        total_milk = entry.mpm + entry.mpe

        if worker not in worker_milk_totals:
            worker_milk_totals[worker] = total_milk
        else:
            worker_milk_totals[worker] += total_milk

    # Add the aggregated data to the worker milk production table
    for worker, total_milk in worker_milk_totals.items():
        doc.append('worker_milk_production', {
            'worker_name': worker,
            'total_milk_produced': total_milk
        })

    # Optionally, save the document
    doc.save()
