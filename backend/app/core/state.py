class ActiveDatasetState:
    def __init__(self):
        self.table_name = None
        self.schema_str = ""
        self.columns = []
        self.profile = {}

    def set_dataset(self, table_name: str, schema_str: str, columns: list, profile: dict = None):
        self.table_name = table_name
        self.schema_str = schema_str
        self.columns = columns
        self.profile = profile or {}

    def clear(self):
        self.table_name = None
        self.schema_str = ""
        self.columns = []
        self.profile = {}


active_dataset = ActiveDatasetState()

