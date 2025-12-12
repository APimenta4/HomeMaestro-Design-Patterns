# Project Architecture

TODO: update diagram with new classes and export image

[High Level Class Diagram (draw.io)](https://app.diagrams.net/#G1Dm2RSYODV8ipJ_am0yr1ROCWjzooqt7y)

![12-12 Architecture Model](assets/architecture-12-12.png)

TODO: "For the final version of the report, it would be good to also include a component diagram in your description of the high-level architecture of the system."

## High Level Software Architecture

![High Level Software Architecture Diagram](assets/software-architecture.png)

## Home Maestro Singleton

![Home Maestro Singleton Diagram](assets/homemaestro-class.png)

# Device, Hub and Automation Classes

![Device and Hub Class Diagrams](assets/device-hub-classes.png)
![Automation Class Diagram](assets/automation-class.png)

# Design Pattern Documentation

# TODO: update patterns, see professor's feedback

## 1️⃣ Singleton

### Problem

As we (initially) decided to start with in-memory state persistance for our application, we needed actual space in memory to save the state, which in our case would be the devices and automations. Therefore, we needed a way to access this state from multiple places in the code.

Using global variables that you pass around in the code, namely lists or key-value pairs, would be a possible solution. However, it wouldn't encapsulate extra logic or behavior that could be of interest to us when persisting state. 
> *Change: in retrospective, this additional encapsulation doesn't really make sense. (for context, refer to the [What we should've done](#what-we-shouldve-done) section). TL;DR: Using raw lists or key-value pairs would've more accurately represented a database and led to a better design.*

To include this additional desired logic, we could create a class that wraps the lists or key-value pairs that we would use to store the state, including any additional logic we desire. However, we would still need to pass around the instance of this class to every part of the code that would need to access it. 

**This requirement, to frequently access a class intance, was one of the main problems we had to solve.**

**The other problem was the fact that the application should always only have a single state. Therefore, even if we could access the class instances mentioned before, there should only ever be one of them, as they are the ones holding application state**

Similarly, we also have the need to access the `MQTTClient` instance around the code, as it is used in multiple places to publish messages to our broker. And in the same manner, there should only ever be a single instance of this class, as it held the connection to the MQTT broker, which should only be established once.

### Pattern

> Change: although we moved forwards with the Singleton pattern, using a proper layered architecture along with Dependency Injection when necessary would lead to a better design. For context, refer to the [Lacking a Proper Service Layer](#lacking-a-proper-service-layer) ending section.

To solve the problems previously mentioned, the Singleton pattern was applied to the classes we wanted to access globally, namely `HomeMaestro`, `NotificationService`, and `MQTTClient`.

We make use of a Python Metaclass (class of a class that defines how a class behaves) to handle the instance creation and control, allowing us to provide Singleton behavior to any class that uses this Metaclass in a clean and reusable way.

Using a Metaclass allows us to model the resulting concrete Singleton classes (HomeMaestro, NotificationService and MQTTClient) exactly as if they were regular classes. The only difference would be that we know beforehand there will only be one instance of them (and therefore their constructor method will only be called once). 

Using a Metaclass also complies with the Open/Closed Principle, as we can add Singleton behavior to any class without modifying its code, and to the Single Responsibility Principle, as the Singleton Metaclass is solely responsible for ensuring the uniqueness of the instance, [as opposed to what is described in many Singleton pattern descriptions](https://refactoring.guru/design-patterns/singleton#pros-cons) *"(Violates the Single Responsibility Principle. The pattern solves two problems at the time.)"*.

**UML Diagram:**

![Singleton UML Diagram](assets/singleton-diagram.png)

**Source code:**

\- [Singleton Metaclass](src/backend/shared/singleton.py) (the important part)

\- [HomeMaestro Class](src/backend/shared/home_maestro.py)

\- [NotificationService Class](src/backend/shared/notification_service.py)

\- [MQTTClient Class](src/backend/shared/mqtt_client.py)


### Consequences

This usage of Singletons allows us to access the global instance of our Singletons from anywhere in the code without needing to pass around instances. For example, we can simplify access to the `HomeMaestro` instance by simply calling `HomeMaestro()` anywhere in the code.

Therefore, by using Singletons, we can easily update or access the single current state of the application or use a service like `MQTTClient` from anywhere in the code.

From the developer perspective, the Singleton pattern is commonly used and well-known, allowing a faster implementation and lowering the project learning curve.

However, a developer who is not acquainted with the design pattern might interpret that we are creating multiple instances of the Singleton class, which can be confusing. For instance:

```python
home_maestro = HomeMaestro() # New object?
```

❓ Fun fact: [Python documentation](https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules) itself recommends using dedicated modules for sharing global variables. Therefore, it is technically possible to implement a Singleton by having that a module that contains a private variable that holds the instance, and a public function that gets/creates the instance and returns it. However, in Python, visibility modifiers are a convention based on naming rules and are not enforced by the language itself, so it would be possible to create multiple instances of the class if the developer is not careful or if something unexpected happens.

## 🏵️ (Method) Decorator

### Problem

Sometimes it is required to extend the behavior of existing objects (or in our case, methods) without modifying their code directly. This also applies when we are free to change the desired implementation, but still want to add the same behavior to multiple objects/methods while extracting duplicate code.

A possible solution is to use inheritance, although this can be limited by the programming language's constraints or can lead to a complex hierarchy.

### Pattern

A simplified version of the Decorator pattern was in our project, in the form of generic Python decorators. Instead of wrapping objects to extend their behavior, as described in the original Decorator pattern, we apply the same concept to functions instead.

One of the generic decorator that we opted to implement is named `validates_exceptions`. It is used to wrap API endpoint handler methods, and it captures any exceptions raised during the execution of the endpoint method and converts them into appropriate HTTP error responses. It also integrates seamlessly with Flask's decorators, as described in the conventional Decorator pattern.

**Structural Explanation**

Under the hood, what's happening inside the API endpoint is exactly the equivalent to:

```python
@devices_api.route("/", methods=["GET"])
def get_devices() -> Response:
    # ... decorator logic ...
        devices = [device.to_dict() for device in home_maestro.devices]
        return make_response(devices)
    # ... decorator logic ...
    # return ...
```

**Source code:**

\- [Validates Exceptions Decorator](src/backend/shared/validates_exceptions.py)

\- [Usage Example in Devices API](src/backend/api/devices_api/devices_api.py)

The motivation behind this choice was the need to extend the behavior of certain methods (e.g., API endpoint handlers) in a reusable, clean and stackable way.

The `validates_exceptions` decorator, in particular, allows us to handle any unexpected errors that may arise during the execution of the endpoint methods, ensuring that the API responds with an appropriate response while logging information for debugging purposes.

### Consequences

**Pros**

- 🟢 Using the method decorator allows us to extend methods behavior without explicitly modifying the original function code, reducing code duplication.

- 🟢 It is possible to stack multiple decorators to combine behaviors, including framework-specific ones (like Flask, in our case).

- 🟢 Enables quickly adding the decorator to new methods as needed (in our case, new endpoints).

- 🟢 Conforms to the Open/Closed and Single Responsibility principles, promoting cleaner code.

- 🟢 Decorators are a well-known, easy to implement and commonly used design pattern in Python, enabling faster development.

**Cons**

- 🔴 Although stacking decorators is possible, they still need to be called in the correct order to function as intended. In our case, we always need to run the decorators before defining the API route with Flask. Example:

```python
@devices_api.route("/", methods=["POST"])
@validates_exceptions
def add_device() -> Response:
```

## 🏭 Simple Factory

Simple Factory method is used to simplify the creation of objects that can be of multiple concrete classes.

This allows us to centralize object creation logic in a single location, making the creation of those concrete objects easier. This code is located on the Factory classes, and simply requires the usage of a "type" argument to determine which concrete class to instantiate.

Although we still need to make chain of "ifs" (or in our case, switch-case statements) to determine which concrete class to instantiate, this logic is now encapsulated within the Factory class, meaning that it won't be scattered all over the code.

Some examples of this pattern can be found in the following Factory classes:

**Source code:**

\- [Hub Factory](src/backend/devices/hubs/hub_factory.py)

\- [Action Factory](src/backend/devices/actions/action_factory.py)

\- [Feature Factory](src/backend/devices/features/feature_factory.py)

\- [Condition Factory](src/backend/devices/conditions/condition_factory.py)

\- [Trigger Factory](src/backend/devices/triggers/trigger_factory.py)

\- [Command Factory](src/backend/devices/commands/command_factory.py)

TODO: add states factory

## Template Method

We make use of the Template Method design pattern to structure well-defined steps of certain interactions with our API.

While creating entities, we always follow a consistent series of steps that are common to all POST endpoints. These steps include verifying the payload, preparing the data, creating the entity, and finally returning the response.

Most of the code for these steps is the same, and for that reason we encapsulated this common logic in abstract base classes, which define the overall structure of the process while allowing subclasses to implement specific details.

Afterwards, we can simply call the general method that calls these steps in order in each API endpoint.

This behavior can be seen in the following classes:

**Source code:**
\- [AutomationCreationAlgorithm](src/backend/api/endpoint_templates/automation_creation_algorithm.py)

\- [DeviceCreationAlgorithm](src/backend/api/endpoint_templates/device_creation_algorithm.py)

\- [EntityCreationAlgorithm](src/backend/api/endpoint_templates/entity_creation_algorithm.py)

Is it called in:

\- [Automations API](src/backend/api/automations_api/automations_api.py)

\- [Devices API](src/backend/api/devices_api/devices_api.py)

# TODO: add publisher subscriber

# TODO: add state

# TODO: add adapter


# dsds

# Project Retrospective

## 🧩 Patterns used

Out of the patterns that were used in the project, we consider that most of them were appropriate for the problems we were trying to solve. Although the Publisher-Subscriber pattern doesn't make a lot of sense in the current state of the project, it still made sense to eventually implement it, as we are planning to move towards real devices that would communicate asynchronously through MQTT messages.

**The exception to the last paragraph would be, in our opinion, the State design pattern used in devices.**

### State Pattern and Real Devices

Given the requirements of the project, separation of different Device states' behavior was not necessary or much benefitial. We were limited to only three states, and the behavior of two of them (offline and error) happened to only be a simple restriction of actions that could be performed on the device, rather than a completely different behavior. 

It was therefore easier to simply check for those states in the methods that required it (if that meant making creating and repeating two conditions for the methods where state was used, we could create a helper function), rather than creating separate classes for each state and delegating the behavior to them, which made the project structure more complex with no real benefit.

A case where state pattern could actually be benefitial and make sense to use would be when we move towards real devices, as those could introduce more states or more complex behaviors. 

**However, in this regard, we also made a fundamental mistake of assuming every Device is a virtual Device**, which would not necessarily be true as we also planned to include real devices in our system, which can't be represented by the current Device class.

**While the current Device class implementation is fine for virtual devices, our "real" devices entity class should not have many of the attributes that are present in the "virtual" devices entity**. For virtual devices, behavior like executing features or sending commands should've been handled by a separate class, namely the one mentioned in the Service Layer section [below](#lacking-a-proper-service-layer).

**Therefore, whether we even needed to store a Device state in the first place was debatable**.

## Lacking a proper Service Layer

Currently, entity classes (Device, Hub, Automation) rely on global Singleton instances (HomeMaetro and MQTTClient, in our case) on some of their methods. This indicates a bad design, as base entity class and the global instance are tightly coupled.

Even if we were to use Dependency Injection to provide the global instance to the entity classes as discussed before in the Singleton section, making them more decoupled and testable, we are still making a fundamental mistake of making a base entity class dependant on the implementation of a global service, which it should not even be aware of. An entity class should not be aware of how to access or use global services, as this violates the Single Responsibility Principle and makes maintenance and testing more difficult.

In our case, we could technically make those service transactions directly inside the API route handlers, although this would break the SRP and DRY principles, since we would be repeating code often and mixing business logic with API handling logic.

### What we should've done

Instead, we should create a new Service Layer for our project (which we are currently lacking). What we currently have is the HomeMaestro class which is working both as the persistance layer and also includes some parts of the service layer.

For example, we would have DeviceService that would be responsible for handling all interactions between the entity classes and the global services (HomeMaestro, MQTTClient, etc..). Ideally, we would also include here the persistence logic for the entities in this same service (even if we are not technically using a database yet, we could still use simple in-memory lists or key-value pairs as the persistance here), and later on if we decided to move towards a proper database solution, we would not need to refactor anything other than the persistance logic inside the service layer.

**This proposed design would also mitigate the need to use the Singleton design pattern, as we could provide the HomeMaestro, MQTTClient or other necessary class instances through Dependency Injection.**

## Conclusion

Designing, iterating and reflecting over the architecture that led to this problem was a valuable learning experience, as we were able to refresh concepts such as having a proper layered architecture and the importance of separation of concerns in software design. Although things *work* so far (due to the lack of complexity of the project), it doesn't mean they are well-designed, maintainable or testable.

Besides that, we were also able to come upon the realization that some of the design patterns we used (namely Singleton and perhaps State design patterns) were not really necessary or were the fruit of lack of knowledge at the time of implementation. Regardless of the cause, these patterns made sense to implement given the match between the problems we had and the problem each pattern solves.

That being said, documenting the patterns as they were being used in this report would also have helped us reflect more on the design choices, detect some of the present flaws sooner and arrive at a better design overall. This is something we will take into account for future projects.
