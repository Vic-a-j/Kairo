<h1 align="center">kairo-engine</h1>

<p align="center">
  <img src="https://raw.githubusercontent.com/Vic-a-j/Kairo/main/images/kairo-img.png" width="400">
</p>

<p align="center">
  <b>Configuration-driven engine that dynamically mutates incoming payloads based on conditional rules defined in YAML or JSON.</b><br>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-blue.svg?style=flat-square"/>
  <img src="https://img.shields.io/github/v/release/Vic-a-j/kairo-engine?style=flat-square"/>
</p>

---

### --Overview--

**Kairo** is a configuration engine that modifies payload requests into a new one. With `Canaries` defined in a YAML-config or JSON-config, you can specify a matching `Condition` that applies `Mutations` if the condition is met i.e - if an path with a value is found. A mutation then applies any mutation given it finds a path and mutates it to a _jmes-path_ search condition. Refer to 'How to Run' and 'Example Usage' for further examples.

---

### --How To Run--

To run the engine, you need to create a **_Kairo()_** instance, load it properly with a yaml or json config - then run any condition or mutation(s) into incoming requests.


E.g -
```
kairo = Kairo()
kairo.load_from_yaml("canaries.yaml")
result = kairo.run({"some": "request"})
````

You can also create your own Condition / Mutations objects dynamically and run it through the Canary evaluator. To do so you first define a Match, and Filter objects to create your condition/mutation instances, initialize a canary object and evaluate it with an incoming payload request as such:

#### 1️⃣ Get your request
```
original_request = {"foo": {"bar": 1, "baz": 2}}
```

#### 2️⃣ Create your Match and Filter objects
```
match_obj = Match(path="foo.bar", with_value=1) # create match condition
filter_obj = Filter(path="foo.bar", to_value="foo.baz") # create filter condition
```

#### 3️⃣ Create your Condition, Mutation, and (optional) added config
```
condition = Condition(match=match_obj)
mutation = Mutation(filter=filter_obj)
config = {"add": "me"}
```

#### 4️⃣ Create Canary object and run evaluation
```
canary = Canary("test_foo_bar_baz", condition=condition, mutations=[mutation], config=config)
new_request = canary.evaluate(original_request, override=False)
```

#### 5️⃣ Result
```
new_request = {
    "foo": {
        "bar": 2,
        "baz": 2
    },
    "add": "me"
}
```

### --- To run it through a YAML-config or JSON-config the format should be as follows:

#### YAML Config:
```
global_config:
  name: (str)

  canaries:
    - name: (str)
      condition:
        match:
          path: (str)
          with_value: (Any)
      mutations:
        - filter:
            path: (str)
            to_value: (str)
        ...
    ...

      config:
          ...
```


#### JSON Config:
```
{
    "global_config": {
        "name": (str),
        "canaries": [
            {
                "name": (str),
                "condition": {
                    "match": {
                        "path": (str),
                        "with_value": (Any)
                    }
                },
                "mutations": [
                    {
                        "filter": {
                            "path": (str),
                            "to_value": (str)
                        }
                    } ...
                ]
            } ...
        ],
        "config": (Any)
    }
}
```

---

### Testing
This is a dockerized **python-3.12** and can be ran with **Makefile** commands as follows:

1) _"make ps"_ -> ```docker-compose ps```

2) _"make build"_ -> ```docker-compose build```

3) _"make build-clean"_ -> ```docker-compose build-clean```

4) _"make exec"_ -> ```docker-compose exec server bash```

5) _"make up"_ -> ```docker-compose up```

6) _"make up-test"_ -> ```docker-compose up test```

7) _"make down"_ -> ```docker-compose down```


Testing can be done inside of the container. Once it's spun up you can exec into it and run tests there.

```
1) Make a build or new clean build.
2) Exec into the container.
3) Inside the container run commands: `python3.12 -m pytest tests`
```

---

### License

Released under the **MIT License** — see [LICENSE](LICENSE).