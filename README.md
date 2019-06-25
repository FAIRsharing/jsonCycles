[![Build Status](https://travis-ci.org/FAIRsharing/jsonCycles.svg?branch=master)](https://travis-ci.org/FAIRsharing/jsonCycles) [![Coverage Status](https://coveralls.io/repos/github/FAIRsharing/jsonCycles/badge.svg?branch=master)](https://coveralls.io/github/FAIRsharing/jsonCycles?branch=master)

### Create and use a virtual environment
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the tool from python (3.6+)
```
from jsonCycles.schemaResolver import SchemaResolver

if __name__ == '__main__':
    schema_url = "https://datatagsuite.github.io/schema/study_schema.json"
    schema_resolver = SchemaResolver(schema_url, 'URL')
    schema_resolver.schemas_to_graph()
    schema_resolver.show()
```

### Run our Jupyter Notebook

jupyter notebook

[notebooks/Finding_jsonCycles.ipynb#](https://github.com/FAIRsharing/jsonCycles/notebooks/Finding_jsonCycles.ipynb#)
