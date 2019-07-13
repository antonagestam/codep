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
def acquire_radius(_state: immutables.Map) -> int:
    return 6_371


@codep.make_partial()
def calculate_pi(_state: immutables.Map) -> float:
    return 3.14


@codep.make_partial(depends=(calculate_pi, acquire_radius))
def calculate_circumference(state: immutables.Map) -> float:
    return 2 * calculate_pi.value(state) * acquire_radius.value(state)


@codep.make_partial(depends=(acquire_radius, calculate_pi))
def calculate_volume(state: immutables.Map) -> float:
    return (4/3) * calculate_pi.value(state) * acquire_radius.value(state) ** 3
    

if __name__ == '__main__':
    circumference, volume = codep.run(calculate_circumference, calculate_volume)
    print(
        f"The circumference of earth is {circumference} km and its volume is " 
        f"{volume} km^3"
    )
```

## Todo

- [ ] Remove `print()`, use logging
- [ ] Concurrent task execution
- [ ] Make pytest run example in readme?
- [ ] Test suite
- [ ] CI
