from app.services.llm_service import GroqClient

def parse_intent(prompt: str, schema: str = "") -> str:
    """
    Dynamically classifies user intent using LLM reasoning and dataset schema context:
    - 'chat': General greetings, small talk, how are you, or system capabilities help.
    - 'dataset_qa': Column explanations, table info, dataset properties, data types, or counts.
    - 'sql': Explicit requests to view/generate/show raw SQL query strings or code.
    - 'analytics': Calculations, aggregations (sums, averages, counts), grouping, or filtering data.
    - 'visualization': Requests to render, show, plot, or draw visual charts, plots, or graphs.
    - 'report': Requests to compile, generate, or download a document/PDF report.
    """
    # Fast bypass for simple greetings
    prompt_strip = prompt.lower().strip("?!. ")
    if prompt_strip in ("hi", "hello", "hey", "greetings", "yo", "good morning", "good afternoon", "good evening"):
        return "chat"

    client = GroqClient()
    
    # Pre-check for strong analytical keywords to enforce database/analytics routing
    prompt_lower = prompt.lower()
    viz_keywords = ('chart', 'graph', 'visualize', 'plot', 'render chart', 'draw chart')
    report_keywords = ('report', 'pdf', 'download', 'export', 'document')
    sql_keywords = ('sql', 'select statement', 'query code', 'postgresql query')
    analytics_keywords = ('analyze', 'analytics', 'trend', 'compare', 'statistics', 'kpi', 'dashboard', 'insights', 'average', 'mean', 'sum', 'total', 'min', 'max', 'group by')
    
    # Retrieve active dataset context if schema is not provided
    if not schema or not schema.strip():
        from app.core.state import active_dataset
        schema = active_dataset.schema_str
        
    schema_context = f"\nAvailable Database Schema:\n{schema}" if schema else ""
    
    llm_prompt = f"""
You are the central intelligence router for a ChatGPT-like Data Analysis dashboard.{schema_context}

Analyze the user's natural language query and dynamically categorize it into exactly one of the following classes:
- 'chat': The user is greeting you, saying hello/bye, asking how you are, or asking general questions unrelated to specific dataset rows (e.g. "What is SQL?", "Explain machine learning", "What is your name?").
- 'dataset_qa': The user is asking about the structure or metadata of the active dataset (e.g., explaining columns, checking data types, asking what tables are available, or asking what columns exist). They are NOT requesting actual data rows or database values.
- 'sql': The user explicitly asks for raw SQL query syntax, SELECT statements, or code.
- 'analytics': The user wants to query, run calculations, group/average fields, find statistical summaries, or extract/list specific data rows or values (e.g., "Give restaurant names", "List all locations", "Show top 10 customers").
- 'visualization': The user explicitly requests a visual graph, chart, plot, line chart, bar chart, or pie chart of the data.
- 'report': The user explicitly requests a compiled PDF, document, report generation, file export, or download.

User Query: "{prompt}"

STRICT RULE: Reply with ONLY one word from: ['chat', 'dataset_qa', 'sql', 'analytics', 'visualization', 'report']. Do not include any punctuation, conversational introduction, or markdown fences.

Category:
"""
    intent = "chat"
    try:
        response = client.generate_text(llm_prompt, options={"temperature": 0.0, "num_predict": 5})
        cleaned = response.strip().lower()
        for cat in ('chat', 'dataset_qa', 'sql', 'analytics', 'visualization', 'report', 'query_with_llm', 'query_database','query_with_llm'):
            if cat in cleaned:
                intent = cat
                break
    except Exception as e:
        print("Intent agent LLM classification failed, defaulting to chat:", e)
        intent = "chat"


    # Enforce routing accuracy override if analytical keywords are present but class is conversational
    if intent in ("chat", "dataset_qa"):
        if any(w in prompt_lower for w in viz_keywords):
            intent = "visualization"
        elif any(w in prompt_lower for w in report_keywords):
            intent = "report"
        elif any(w in prompt_lower for w in sql_keywords):
            intent = "sql"
        elif any(w in prompt_lower for w in analytics_keywords):
            intent = "analytics"

    print(f"ROUTING INTENT DETECTED: {intent} (User query: {prompt})")
    return intent


