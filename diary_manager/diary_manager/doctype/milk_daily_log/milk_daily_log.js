// Copyright (c) 2024, nani-samireddy and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Milk Daily Log", {
// 	refresh(frm) {

// 	},
// });

// frappe.ui.form.on('Milk Entry Log', {
//     validate: function(frm) {
//         let total_cow_milk = 0;
//         let total_buffalo_milk = 0;

//         frm.doc.entries.forEach(entry => {
//             if (entry.animal_tag) {
//                 frappe.db.get_value('Animal', entry.animal_tag, 'type', (r) => {
//                     if (r && r.type) {
//                         if (r.type.toLowerCase() === 'cow') {
//                             total_cow_milk += entry.milk_in_morning + entry.milk_in_evening;
//                         } else if (r.type.toLowerCase() === 'buffalo') {
//                             total_buffalo_milk += entry.milk_in_morning + entry.milk_in_evening;
//                         }
//                     }
//                 });
//             }
//         });

//         // Wait a moment for all async get_value calls to complete
//         setTimeout(() => {
//             frm.set_value('total_cow_milk', total_cow_milk);
//             frm.set_value('total_buffalo_milk', total_buffalo_milk);
//         }, 1000);
//     }
// });

frappe.ui.form.on('Milk Daily Log', {
	refresh: function (frm) {
		calculate_total_milk_production(frm);
	},
	milk_log_table_add: function (frm, cdt, cdn) {
		calculate_total_milk_production(frm);
	},
	milk_log_table_remove: function (frm, cdt, cdn) {
		calculate_total_milk_production(frm);
	},
	milk_log_table_on_change: function (frm, cdt, cdn) {
		calculate_total_milk_production(frm);
	}
});

function calculate_total_milk_production(frm) {
	let worker_milk_totals = {};

	frm.doc.milk_log_table.forEach(function (entry) {
		let worker = entry.worker_name;
		let total_milk = (entry.mpm || 0) + (entry.mpe || 0);

		if (!worker_milk_totals[worker]) {
			worker_milk_totals[worker] = total_milk;
		} else {
			worker_milk_totals[worker] += total_milk;
		}
	});

	frm.clear_table('worker_milk_production');

	for (let worker in worker_milk_totals) {
		let total_milk = worker_milk_totals[worker];
		let child = frm.add_child('worker_milk_production');
		child.worker_name = worker;
		child.total_milk_produced = total_milk;
	}

	frm.refresh_field('worker_milk_production');
}

