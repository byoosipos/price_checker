// Copyright (c) 2025, byoosicom and contributors
// For license information, please see license.txt

frappe.query_reports["Customer Ratings"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"reqd": 1
		},
		{
			"fieldname": "min_rating",
			"label": __("Minimum Rating"),
			"fieldtype": "Float",
			"default": 1.0
		},
		{
			"fieldname": "max_rating",
			"label": __("Maximum Rating"),
			"fieldtype": "Float",
			"default": 5.0
		},
		{
			"fieldname": "search_term",
			"label": __("Search in Feedback"),
			"fieldtype": "Data",
			"description": "Search for keywords in feedback text"
		}
	],
	
	"formatter": function(value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		
		// Color-code average ratings
		if (column.fieldname === "avg_rating") {
			var color = "";
			if (value >= 4.5) color = "green";
			else if (value >= 3.5) color = "blue";
			else if (value >= 2.5) color = "orange";
			else if (value > 0) color = "red";
			
			if (color) {
				value = `<span style="color: ${color}; font-weight: bold;">${value}</span>`;
			}
		}
		
		return value;
	},
	
	"onload": function(report) {
		// Add star distribution chart after the main chart
		report.page.add_inner_button(__('Show Star Distribution'), function() {
			show_star_distribution(report);
		});
		
		// Add a button to export the data
		report.page.add_inner_button(__('Export Detailed Data'), function() {
			export_detailed_report(report);
		});
	}
};

function show_star_distribution(report) {
	if (!report.chart || !report.chart.star_data) {
		frappe.msgprint(__('No star distribution data available'));
		return;
	}
	
	// Create a dialog with a pie chart
	var d = new frappe.ui.Dialog({
		title: __('Rating Distribution'),
		fields: [
			{
				fieldtype: 'HTML',
				fieldname: 'chart_area'
			}
		],
		size: 'large'
	});
	
	d.show();
	
	// Create pie chart in the dialog
	setTimeout(function() {
		new frappe.Chart(d.fields_dict.chart_area.$wrapper.find('.chart-container')[0], {
			data: report.chart.star_data,
			type: 'pie',
			height: 300,
			colors: ['#ff5858', '#ffb058', '#f8d85b', '#a5ca7b', '#66bb6a']
		});
		
		// Add a summary table below the chart
		var star_data = report.chart.star_data;
		var total = star_data.datasets[0].values.reduce((a, b) => a + b, 0);
		
		var $table = $(`<div class="table-responsive" style="margin-top: 20px">
			<table class="table table-bordered">
				<thead>
					<tr>
						<th>Rating</th>
						<th>Count</th>
						<th>Percentage</th>
					</tr>
				</thead>
				<tbody></tbody>
			</table>
		</div>`);
		
		var $tbody = $table.find('tbody');
		for (var i = 0; i < star_data.labels.length; i++) {
			var count = star_data.datasets[0].values[i];
			var percentage = total ? (count / total * 100).toFixed(1) : 0;
			
			$tbody.append(`<tr>
				<td>${star_data.labels[i]}</td>
				<td>${count}</td>
				<td>${percentage}%</td>
			</tr>`);
		}
		
		d.fields_dict.chart_area.$wrapper.append($table);
		
	}, 300);
}

function export_detailed_report(report) {
	// Get data for export
	frappe.call({
		method: "frappe.desk.query_report.run",
		args: {
			report_name: report.report_name,
			filters: report.get_values()
		},
		callback: function(r) {
			if (!r.message) return;
			
			var data = r.message.result;
			var columns = r.message.columns;
			
			// Convert to format suitable for CSV
			var csv_data = [];
			var headers = columns.map(col => col.label);
			csv_data.push(headers);
			
			data.forEach(function(row) {
				var csv_row = columns.map(col => row[col.fieldname]);
				csv_data.push(csv_row);
			});
			
			// Download CSV
			frappe.tools.download_csv(csv_data, report.report_name + '.csv');
		}
	});
}
