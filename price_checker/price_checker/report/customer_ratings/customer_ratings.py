# Copyright (c) 2025, byoosicom and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import getdate, add_months, today, formatdate
from datetime import datetime, timedelta


def execute(filters=None):
	if not filters:
		filters = {}

	# Define columns for the report
	columns = [
		{
			"fieldname": "created_on",
			"label": "Created On",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "avg_rating",
			"label": "Average Rating",
			"fieldtype": "Float",
			"precision": 2,
			"width": 120
		},
		{
			"fieldname": "total_ratings",
			"label": "Total Ratings",
			"fieldtype": "Int",
			"width": 120
		},
		{
			"fieldname": "one_star",
			"label": "1 Star",
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "two_star",
			"label": "2 Stars",
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "three_star",
			"label": "3 Stars",
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "four_star",
			"label": "4 Stars",
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "five_star",
			"label": "5 Stars",
			"fieldtype": "Int",
			"width": 80
		},
		{
			"fieldname": "common_issues",
			"label": "Common Issues",
			"fieldtype": "Data",
			"width": 200
		}
	]

	# Apply date filters
	from_date = filters.get("from_date") or add_months(today(), -1)
	to_date = filters.get("to_date") or today()
	
	# Query the database to get ratings data
	ratings_data = frappe.db.sql("""
		SELECT 
			DATE(creation) as created_on,
			AVG(exact_rating) as avg_rating,
			COUNT(*) as total_ratings,
			SUM(CASE WHEN ROUND(exact_rating) = 1 THEN 1 ELSE 0 END) as one_star,
			SUM(CASE WHEN ROUND(exact_rating) = 2 THEN 1 ELSE 0 END) as two_star,
			SUM(CASE WHEN ROUND(exact_rating) = 3 THEN 1 ELSE 0 END) as three_star,
			SUM(CASE WHEN ROUND(exact_rating) = 4 THEN 1 ELSE 0 END) as four_star,
			SUM(CASE WHEN ROUND(exact_rating) = 5 THEN 1 ELSE 0 END) as five_star
		FROM 
			`tabRatings` 
		WHERE 
			docstatus = 1
			AND DATE(creation) BETWEEN %s AND %s
			{additional_conditions}
		GROUP BY 
			DATE(creation)
		ORDER BY 
			DATE(creation) DESC
	""".format(
		additional_conditions=get_additional_conditions(filters)
	), (from_date, to_date), as_dict=1)
	
	# Process data for visualization
	data = process_data(ratings_data, from_date, to_date)
	
	# Add chart data
	chart = get_chart_data(data)
	
	# Add summary
	report_summary = get_report_summary(data)
	
	# Get top issues from feedback
	add_feedback_analysis(data, from_date, to_date)
	
	return columns, data, None, chart, report_summary


def get_additional_conditions(filters):
	conditions = ""
	if filters.get("min_rating"):
		conditions += " AND exact_rating >= {0}".format(filters.get("min_rating"))
	if filters.get("max_rating"):
		conditions += " AND exact_rating <= {0}".format(filters.get("max_rating"))
	if filters.get("search_term"):
		conditions += """ AND feedback_reason LIKE '%{0}%'""".format(filters.get("search_term"))
	return conditions


def process_data(ratings_data, from_date, to_date):
	# Ensure we have data points for all dates in the range
	all_dates = []
	current_date = getdate(from_date)
	to_date = getdate(to_date)
	
	while current_date <= to_date:
		all_dates.append(current_date.strftime("%Y-%m-%d"))
		current_date = current_date + timedelta(days=1)
	
	# Convert ratings data to dict by date
	rating_dict = {}
	for row in ratings_data:
		if isinstance(row.get("created_on"), datetime) or isinstance(row.get("created_on"), str):
			date_str = row.get("created_on").strftime("%Y-%m-%d") if isinstance(row.get("created_on"), datetime) else row.get("created_on")
			rating_dict[date_str] = row
	
	# Create complete dataset including dates with no ratings
	processed_data = []
	for date in all_dates:
		if date in rating_dict:
			processed_data.append(rating_dict[date])
		else:
			processed_data.append({
				"created_on": date,
				"avg_rating": 0,
				"total_ratings": 0,
				"one_star": 0,
				"two_star": 0,
				"three_star": 0,
				"four_star": 0,
				"five_star": 0
			})
	
	return processed_data


def get_chart_data(data):
	# Use dictionary access (row["created_on"]) instead of attribute access
	labels = []
	for row in data:
		date_val = row.get("created_on")
		if isinstance(date_val, datetime):
			labels.append(formatdate(date_val, "d-MMM"))
		elif isinstance(date_val, str):
			try:
				labels.append(formatdate(getdate(date_val), "d-MMM"))
			except:
				labels.append(date_val)  # Fallback to the original string
		else:
			labels.append("")  # Empty label for invalid dates
	
	avg_ratings = [row.get("avg_rating") or 0 for row in data]
	
	# Prepare data for star distribution
	datasets = [
		{
			"name": "Average Rating",
			"values": avg_ratings
		}
	]
	
	# For the star distribution chart
	star_labels = ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"]
	star_values = [
		sum(row.get("one_star") or 0 for row in data),
		sum(row.get("two_star") or 0 for row in data),
		sum(row.get("three_star") or 0 for row in data),
		sum(row.get("four_star") or 0 for row in data),
		sum(row.get("five_star") or 0 for row in data)
	]
	
	# Return chart configuration
	return {
		"data": {
			"labels": labels,
			"datasets": datasets
		},
		"type": "line",
		"lineOptions": {
			"regionFill": 1
		},
		"axisOptions": {
			"yAxisMode": "tick"
		},
		"colors": ["#5e64ff"],
		"height": 280,
		"star_data": {
			"labels": star_labels,
			"datasets": [{
				"values": star_values
			}]
		}
	}


def get_report_summary(data):
	# Calculate overall statistics
	total_reviews = sum(row.get("total_ratings") or 0 for row in data)
	if total_reviews == 0:
		return []
	
	avg_rating = sum((row.get("avg_rating") or 0) * (row.get("total_ratings") or 0) for row in data) / total_reviews if total_reviews else 0
	five_star_percentage = sum(row.get("five_star") or 0 for row in data) * 100 / total_reviews if total_reviews else 0
	low_rating_percentage = sum((row.get("one_star") or 0) + (row.get("two_star") or 0) for row in data) * 100 / total_reviews if total_reviews else 0
	
	return [
		{
			"value": "{:.2f}".format(avg_rating),
			"label": "Average Rating",
			"datatype": "Float",
			"indicator": get_indicator(avg_rating)
		},
		{
			"value": total_reviews,
			"label": "Total Reviews",
			"datatype": "Int"
		},
		{
			"value": "{:.1f}%".format(five_star_percentage),
			"label": "5 Star Ratings",
			"datatype": "Float",
			"indicator": "green" if five_star_percentage > 70 else "orange"
		},
		{
			"value": "{:.1f}%".format(low_rating_percentage),
			"label": "Low Ratings (1-2)",
			"datatype": "Float",
			"indicator": "red" if low_rating_percentage > 20 else ("orange" if low_rating_percentage > 10 else "green")
		}
	]


def get_indicator(value):
	if value >= 4.5:
		return "green"
	elif value >= 3.5:
		return "blue"
	elif value >= 2.5:
		return "orange"
	else:
		return "red"


def add_feedback_analysis(data, from_date, to_date):
	# Get feedback data for ratings lower than 5
	feedback_data = frappe.db.sql("""
		SELECT 
			feedback_reason 
		FROM 
			`tabRatings` 
		WHERE 
			docstatus = 1
			AND DATE(creation) BETWEEN %s AND %s
			AND exact_rating < 5
			AND feedback_reason IS NOT NULL
			AND feedback_reason != ''
		ORDER BY 
			creation DESC
	""", (from_date, to_date), as_dict=1)
	
	# Analyze common issues in feedback
	feedback_texts = [row.feedback_reason for row in feedback_data]
	common_issues = analyze_feedback(feedback_texts)
	
	# Add common issues to data rows
	for row in data:
		row["common_issues"] = common_issues


def analyze_feedback(feedback_texts):
	if not feedback_texts:
		return "No feedback available"
	
	# Simple keyword analysis for demonstration
	# In a real implementation, more sophisticated NLP techniques would be used
	keywords = {
		"slow": 0, "wait": 0, "waiting": 0, "delay": 0,
		"price": 0, "expensive": 0, "cost": 0,
		"error": 0, "wrong": 0, "incorrect": 0, "mistake": 0,
		"interface": 0, "difficult": 0, "confusing": 0, "hard": 0,
		"scan": 0, "barcode": 0, "scanning": 0
	}
	
	# Count occurrences of keywords
	for text in feedback_texts:
		if not text:
			continue
		text = text.lower()
		for keyword in keywords:
			if keyword in text:
				keywords[keyword] += 1
	
	# Group keywords into categories
	categories = {
		"Performance Issues": keywords["slow"] + keywords["wait"] + keywords["waiting"] + keywords["delay"],
		"Price Concerns": keywords["price"] + keywords["expensive"] + keywords["cost"],
		"Accuracy Problems": keywords["error"] + keywords["wrong"] + keywords["incorrect"] + keywords["mistake"],
		"Usability Issues": keywords["interface"] + keywords["difficult"] + keywords["confusing"] + keywords["hard"],
		"Scanner Problems": keywords["scan"] + keywords["barcode"] + keywords["scanning"]
	}
	
	# Get top 2 categories
	sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
	top_categories = [cat[0] for cat in sorted_categories[:2] if cat[1] > 0]
	
	if top_categories:
		return ", ".join(top_categories)
	else:
		return "No common issues identified"
