### Create and use a virtual environment
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the tool
```
from jsonCycles.graphCycles import Graph

schema_URL = "https://datatagsuite.github.io/schema/study_schema.json" # can also be a file
schema_from_url = SchemaResolver(schema_URL, 'url')
raw_cycles = schema_from_url.schemas_to_graph()
    item_positions = list(schema_from_url.output.keys())
    for cycle in raw_cycles:
        local_cycle = []
        for item in cycle:
            local_cycle.append(item_positions[item])
        print("Cycle:", local_cycle)
```