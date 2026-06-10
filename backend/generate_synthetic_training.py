import os
import json
from app.core.state import active_dataset

def main():
    print("Starting synthetic training dataset generator...")

    # Determine schema context
    schema_str = active_dataset.schema_str
    table_name = active_dataset.table_name or "sales"

    if not schema_str:
        # Fallback default schema
        schema_str = f"""{table_name}(
    id INTEGER,
    product_name TEXT,
    region TEXT,
    sales FLOAT,
    votes INTEGER,
    sale_date DATE
)"""

    examples = []

    # 1. Chat Examples
    chat_prompts = [
        ("Hello, who are you?", "Hello! I am Genora AI, your friendly conversational data analyst assistant. You can ask me to analyze datasets, render interactive charts, generate SQL queries, or compile reports!"),
        ("What is your name?", "I am Genora AI, a conversational data analysis assistant designed to help you explore and understand your datasets."),
        ("Explain machine learning in simple terms.", "Machine learning is a subset of artificial intelligence where computers learn patterns from historical data to make predictions or decisions on new data, without being explicitly programmed."),
        ("What is a relational database?", "A relational database organizes data into tables with columns and rows, establishing relationships between them using keys (like primary and foreign keys) for structured querying using SQL."),
        ("What is SQL?", "SQL stands for Structured Query Language. It is the standard language used to communicate with, manage, and query relational database management systems."),
        ("How can you help me?", "I can help you by answering natural language questions about your active dataset, generating SQL queries, plotting visual graphs (like bar, line, boxplots, heatmaps), and compiling reports."),
        ("What are the best practices for data cleaning?", "Best practices include handling missing values, removing duplicates, normalizing column naming, parsing dates correctly, and filtering outliers."),
        ("What is the difference between a bar chart and histogram?", "A bar chart compares discrete categories (e.g. Sales by Region), whereas a histogram shows the distribution of continuous numerical data grouped into bins."),
        ("Can you write a python script?", "I specialize in data analysis and SQL generation, but I can also help explain concepts or generate Python blocks for data visualizer interfaces if requested."),
        ("How do I upload a dataset?", "You can upload spreadsheets (CSV or Excel) directly in the sidebar dropzone. I will parse it, save it, and analyze the columns automatically.")
    ]
    for prompt, resp in chat_prompts:
        examples.append({
            "instruction": prompt,
            "schema": "",
            "intent": "chat",
            "sql": "",
            "response": resp
        })

    # 2. Dataset QA Examples
    dataset_qa_prompts = [
        ("What columns are in this table?", f"Based on the active dataset table '{table_name}', the available columns and their data types are defined in the schema:\n{schema_str}"),
        ("Explain the columns of this table", f"The table '{table_name}' contains the columns listed in the schema. You can perform calculations, filter by specific attributes, or generate visual trends across these fields."),
        ("How many columns are there?", f"The dataset has the columns defined in the schema: {schema_str}"),
        ("What table is currently active?", f"The active table currently loaded in the connection workspace is '{table_name}'."),
        ("Show me the data types of the columns.", f"Here are the data types for the active dataset columns:\n{schema_str}"),
        ("What is the row count?", f"Please check the dataset statistics summary in the connection panel for the exact row count of the uploaded spreadsheet."),
        ("Is there a sales column in the dataset?", f"Yes, the columns present in the table are specified in the active schema:\n{schema_str}"),
        ("Can you show me the schema structure?", f"Certainly! Here is the active schema structure:\n{schema_str}"),
        ("Explain the structure of this database.", f"The database has an active table '{table_name}' structured with the columns and types as follows:\n{schema_str}"),
        ("Do we have a date column here?", f"Yes, dates or times can be found in the schema columns:\n{schema_str}")
    ]
    for prompt, resp in dataset_qa_prompts:
        examples.append({
            "instruction": prompt,
            "schema": schema_str,
            "intent": "dataset_qa",
            "sql": "",
            "response": resp
        })

    # 3. SQL Examples
    sql_prompts = [
        ("Generate a SQL query to get all columns from the table", f"SELECT * FROM {table_name};"),
        ("Write SQL to find maximum sales", f"SELECT MAX(sales) AS max_sales FROM {table_name};"),
        ("Show PostgreSQL code for top 10 records", f"SELECT * FROM {table_name} LIMIT 10;"),
        ("SQL query to count rows", f"SELECT COUNT(*) AS total_rows FROM {table_name};"),
        ("Write SQL query to group by region", f"SELECT region, SUM(sales) AS total_sales FROM {table_name} GROUP BY region;"),
        ("Show me the SQL for average votes", f"SELECT AVG(votes) AS average_votes FROM {table_name};"),
        ("Generate SQL to select product_name where sales are greater than 100", f"SELECT product_name, sales FROM {table_name} WHERE sales > 100;"),
        ("SQL statement to sort by sale_date descending", f"SELECT * FROM {table_name} ORDER BY sale_date DESC;"),
        ("Give SQL query to find unique product names", f"SELECT DISTINCT product_name FROM {table_name};"),
        ("Write SQL query to filter by region North and count products", f"SELECT COUNT(*) AS count FROM {table_name} WHERE region = 'North';")
    ]
    for prompt, sql in sql_prompts:
        examples.append({
            "instruction": prompt,
            "schema": schema_str,
            "intent": "sql",
            "sql": sql,
            "response": f"Here is the raw PostgreSQL query compiled for your request:\n\n```sql\n{sql}\n```"
        })

    # 4. Analytics Examples
    analytics_prompts = [
        ("Give restaurant names", f"SELECT product_name FROM {table_name} LIMIT 100;", "Here are the product/restaurant names retrieved from the dataset:"),
        ("List all locations", f"SELECT DISTINCT region FROM {table_name};", "Here is the list of unique locations/regions represented in the active database:"),
        ("Show top 10 customers", f"SELECT product_name, sales FROM {table_name} ORDER BY sales DESC LIMIT 10;", "Here are the top 10 records sorted by sales volume:"),
        ("Calculate average sales by product_name", f"SELECT product_name, AVG(sales) AS avg_sales FROM {table_name} GROUP BY product_name;", "The average sales metric has been calculated per product category:"),
        ("Generate analytics between restaurant_name and votes", f"SELECT product_name, SUM(votes) AS total_votes FROM {table_name} GROUP BY product_name ORDER BY total_votes DESC;", "We analyzed votes across different product/restaurant categories. Here is the summary breakdown:"),
        ("Compare sales and region", f"SELECT region, SUM(sales) AS total_sales FROM {table_name} GROUP BY region;", "This analysis compares total sales performance across the geographical regions:"),
        ("Analyze latitude and longitude", f"SELECT * FROM {table_name} LIMIT 100;", "We retrieved latitude and longitude coordinates to analyze location distribution maps:"),
        ("Find highest sales value", f"SELECT * FROM {table_name} ORDER BY sales DESC LIMIT 1;", "The record representing the highest sales value has been identified:"),
        ("Group sales by sale_date month", f"SELECT DATE_TRUNC('month', sale_date) AS month, SUM(sales) AS total_sales FROM {table_name} GROUP BY month ORDER BY month;", "Here is the month-over-month trend analysis for sales metrics:"),
        ("Count total votes", f"SELECT SUM(votes) AS total_votes FROM {table_name};", "The aggregate sum of votes across all records is calculated below:")
    ]
    for prompt, sql, resp in analytics_prompts:
        examples.append({
            "instruction": prompt,
            "schema": schema_str,
            "intent": "analytics",
            "sql": sql,
            "response": f"{resp}\n\n```sql\n{sql}\n```"
        })

    # 5. Visualization Examples
    visualization_prompts = [
        ("Plot a bar chart of sales by region", f"SELECT region, SUM(sales) AS total_sales FROM {table_name} GROUP BY region;", "Here is the comparison bar chart showing sales performance by geographical region:"),
        ("Show a line chart of sales trend over time", f"SELECT sale_date, sales FROM {table_name} ORDER BY sale_date;", "Here is the chronological trend line chart showing sales progress over time:"),
        ("Draw a pie chart of sales by product_name", f"SELECT product_name, SUM(sales) AS total_sales FROM {table_name} GROUP BY product_name LIMIT 5;", "Here is the compositional pie chart representing the sales breakdown:"),
        ("Plot a histogram of votes distribution", f"SELECT votes FROM {table_name};", "Here is the frequency distribution histogram of votes across all entries:"),
        ("Show a scatter plot of sales vs votes", f"SELECT sales, votes FROM {table_name};", "Here is the scatter plot visualizing the distribution and correlation of sales vs votes:"),
        ("Render a correlation matrix heatmap", f"SELECT * FROM {table_name};", "Here is the correlation heatmap matrix displaying correlation coefficients between numerical fields:"),
        ("Generate a boxplot of sales by region", f"SELECT region, sales FROM {table_name};", "Here is the boxplot showing the distribution, median, and outliers of sales grouped by region:"),
        ("Plot a heatmap of votes", f"SELECT * FROM {table_name};", "Here is the correlation heatmap matrix representing variable distribution:"),
        ("Compare sales and votes on a scatter graph", f"SELECT sales, votes FROM {table_name};", "Here is the scatter distribution showing the relationship between sales volume and user votes:"),
        ("Draw a histogram of sales", f"SELECT sales FROM {table_name};", "Here is the histogram representing the distribution of sales values:")
    ]
    for prompt, sql, resp in visualization_prompts:
        examples.append({
            "instruction": prompt,
            "schema": schema_str,
            "intent": "visualization",
            "sql": sql,
            "response": f"{resp}\n\n```sql\n{sql}\n```"
        })

    # 6. Report Examples
    report_prompts = [
        ("Create report for generated analytics", f"SELECT * FROM {table_name} LIMIT 100;", "### 📄 BI PDF Report Compiled\n\nI have generated business insights and structured the database query output into a formal report template containing an Executive Summary, KPI cards, trend charts, and recommendations. Click the button below to download the compiled PDF report."),
        ("Generate a PDF report", f"SELECT * FROM {table_name} LIMIT 100;", "### 📄 BI PDF Report Compiled\n\nYour downloadable PDF report has been compiled successfully. It includes an executive summary of the dataset and analytical findings."),
        ("Download report for sales by region", f"SELECT region, SUM(sales) AS total_sales FROM {table_name} GROUP BY region;", "### 📄 BI PDF Report Compiled\n\nI have compiled the regional sales report. You can download the complete document immediately by clicking the Download PDF Report button below.")
    ]
    for prompt, sql, resp in report_prompts:
        examples.append({
            "instruction": prompt,
            "schema": schema_str,
            "intent": "report",
            "sql": sql,
            "response": resp
        })

    # Save to file
    os.makedirs("training_data", exist_ok=True)
    out_path = "training_data/synthetic_training.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(examples, f, indent=2)

    print(f"Successfully generated {len(examples)} synthetic training examples at: {out_path}")

if __name__ == "__main__":
    main()
