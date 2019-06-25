[![Build Status](https://travis-ci.org/FAIRsharing/jsonCycles.svg?branch=master)](https://travis-ci.org/FAIRsharing/jsonCycles) [![Coverage Status](https://coveralls.io/repos/github/FAIRsharing/jsonCycles/badge.svg?branch=master)](https://coveralls.io/github/FAIRsharing/jsonCycles?branch=master)

### Create and use a virtual environment
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the tool
```
from jsonCycles.schemaResolver import SchemaResolver

if __name__ == '__main__':
    schema_url = "https://datatagsuite.github.io/schema/study_schema.json"
    schema_resolver = SchemaResolver(schema_url, 'URL')
    schema_resolver.resolve_network()
    schema_resolver.schemas_to_graph()
    item_positions = list(schema_resolver.output.keys())
    for cycle in schema_resolver.raw_cycles:
        local_cycle = []
        for item in cycle:
            local_cycle.append(item_positions[item])
        print("Cycle:", local_cycle)
```

