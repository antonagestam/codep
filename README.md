# codep

A light-weight framework for defining and running dependent tasks. By building a
dependency graph between tasks, the runner makes sure that tasks that are
required by multiple dependants are only run once and reuses the results.

## Usage

In the example below the `calculate_circumference` and `calculate_volume` tasks
both depend on the `acquire_radius` and `calculate_pi` tasks. The runner will
infer that from the dependency graph and run them before.

```python
import codep
import immutables


@codep.make_partial()
def acquire_radius(state: immutables.Map) -> immutables.Map:
    return state.set("radius", 6_371)


@codep.make_partial()
def calculate_pi(state: immutables.Map) -> immutables.Map:
    return state.set("pi", 3.14)


@codep.make_partial(depends=(calculate_pi, acquire_radius))
def calculate_circumference(state: immutables.Map) -> immutables.Map:
    return state.set("circumference", 2 * state["pi"] * state["radius"])


@codep.make_partial(depends=(acquire_radius, calculate_pi))
def calculate_volume(state: immutables.Map) -> immutables.Map:
    return state.set("volume", (4/3) * state["pi"] * state["radius"] ** 3)
    

if __name__ == '__main__':
    r1, r2 = codep.run(calculate_circumference, calculate_volume)
    circumference = r1.state["circumference"]
    volume = r2.state["volume"]
    print(
        f"The circumference of earth is {circumference} km and its volume is " 
        f"{volume} km^3"
    )
```

## Todo

- [ ] Make Partial a Generic, and make tasks only able to return a value.
      `Partial.apply` should instead assign the result to the state which
      becomes a mapping `Type[Partial] -> Any`.
- [ ] Remove `print()`, use logging
- [ ] Concurrent task execution
