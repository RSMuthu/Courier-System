# Courier Services

## Models Used
1. Product
2. Offer
3. Vehicle
4. Delivery Service

#### Product

**NOTE:** _Please note that the phrases "Product" and "Package" are interchangeably used as this is Courier system_

This Model holds the information about the certain product. \
The information includes:
- Base delivery cost
- Product name
- Offer
- Weight
- Distance to the delivery destination
- Time in which the product shall be delivered

The Base delivery cost is associated with each product (although problem states it is globally set) because, every product could vary in type (probably a glass item), size, etc and the base cost could differ accordingly. \
This model provides with necessary functionality for calculating the estimation cost for the delivery.\
The discount information are provided by Offer Model

#### Offer
This Model is used for the functionalities and validations related to the handling the Offers. \
The details of the available Offers are stored in a config file. \
Ideal way to set up the available offers and manage them is to have as DB table entries but considering the scale of application, normal config file is used

#### Vehicle
This Model holds information about the Vehicles. The info includes:
- Number of vehicles
- Maximum Load handling capacity of the vehicles
- The Speed in which the Vehicles shall move for delivery

The vehicles and their availabilities are based on the time (which is set to the completion time of their previous delivery).\
The Vehicles are used for dispatching the delivery and the vehicle selected for the next dispatch is set based on a priority queue and the priority is set on the vehicle available time. \
Min heap is used for this priority queue.

#### Delivery Service
This Model helps is triggering the delivery of the list of packages. \
It handles the selection of packages that are to be delivered by a single vehicle. \
The Base criteria for selection of packages (as given by problem statement) is in order:
1. Maximum number of packages
2. Heavier packages
3. Packages that can be shipped faster

#### Delivery Package Selection Implementation Ideas
##### 1. Brute Force Logic *__(Depreciated)__*
Start out from the combinations with maximum possible number of items and then drive down to the solution. But the Logic for package selection is more of NP-hard problem. So brute force solution could cost us a lot. Optimisation is required if application scales up. Few options for optimisation -  Dynamic programming, Integer programming (a field of mathematics)

##### 2. Integer Programming Logic
As a step to optimisation, a little exploration was done on Integer Programming; field of Mathematics.\
This Package selection problem can be posed as an integer programming problem. \
In Integer programming (mathematical optimization program), some or all of the variables are restricted to be integers.\
While using this, we usally model the decisions as discete decision variables (linear function), set of constraints as fesible decision variables (linear constraint) and variable domains holding real values. This resulting model is solved using Integer Programming algorithm (for this, SCIP solver is used)

Lets introduce $x_i$ where $i \in I$ to represent whether product $i$ is selected. \
If $x_i = 1$ then product $i$ is selected, else $x_i = 0$ and product $i$ is not selected;\
$x_i \in \lbrace0, 1\rbrace, i = 0, 1, 2, ... n$ & $i \in I$ . $W$ is the threshold weightpossible to carry. \
$w_i$ is the wight of product $i$ and $d_i$ is the delivery distance of product $i$. \
As all package has unit value, $u_i = 1, \forall i \in I$ \
With that said, each objectives and associated constraints are:

*__Objective 1:__ maximize the number of package picked such that total weight is within the threshold*

$$
ValueObjective = max \sum_{i \in I} u_ix_i \ni \sum_{i \in I} w_ix_i \le W
$$

*__Objective 2:__ maximize package weights after previous objective is met*

$$
WeightObjective = max \sum_{i \in I} x_iw_i , \forall productlist \in ValueObjective
$$

*__Objective 3:__ minimize the maximum distance in each dispatch after previous objective is met*

$$
DistanceObjective = min \lbrace max \lbrace x_id_i, i \in I\rbrace , \forall productlist \in WeightObjective \rbrace
$$

By the end of our 3 objective completions,

$$
DistanceObjective \subseteq WeightObjective \subseteq ValueObjective \subseteq PackageList
$$

### Application Useage
This is a command line based application with `poetry` as package manager.\
There are two poetry scripts to trigger the application

> `$ poetry run courier`

 Triggers the application and lets the user input the information. As the user provides the data, it will validated immediately and then, the courier delivery gets triggered

 > `$ poetry run courier-cli -f "examples/sample1.json"`

Triggers the application but instead of giving control to user, the necessary data is fed via json file.\
The validation happens over the data loaded from the json file and then the courier delivery triggers

#### Testing
The following command is used to trigger the test runs for the application.

> `$ poetry run pytest`

For the time being, the Test setup done is simple. A wide scope is available for update on this space in the future. \
For example, the resources are created everytime as needed on different test files. This could be better with proper `fixtures` based setup.

#### Docker
Added a minimal docker setup along with this (not an optimised setup; security aspects are not lookedup).\
Ofcourse, Docker setup is not effectively tested but it still works on interactive bash.\
Once the docker image is built, you can enter interactive mode and use the application as mentioned before.

> `$ docker build -t courier-build .

This will create an image.

> docker run -it courier-build /bin/bash

With this, we can enter the interactive bash terminal of the image created before.\
After entering, we can just use the application as mentioned before.

### Few Future Considerations for development
- Package/Product selection logic is updated to use Integer Programming solver with model based resolution. \
But it still needs to be clearly experimented futher to find the optimal solver suited for our usecase.
- The Test files are creating & using the resources on the fly. Update the test files to use proper `fixtures` and a strutured execution flow using parameterized tests and pytest markers
- So far, only 'Black' is added to the codebase which helps to prettify the code. But we need to add linter as well to the application (probably, pylint)
- The available Offer details are stored as Config for now. This needs to be updated to use database that way, the data management would be easier and the Offer related data would persist in DB. Ofcourse, this will very much matter when application scales up.
- The `dockerfile` can also be cleaned (add another stage to split the application working from the `python-base`) & updated with the security aspects & the Entry point can also be setup with `tini` (or something similar).

### Learning Takeaways
While working on this, most time I spent was on reading through Mixed Integer Programming, Constraint Programming and few other concepts of optimization problem. \
Althought I am still a beginner in this field, I just got curious and exploring in my free time. I had a good learn on this interesting things. I am further trying to learn deeper on the different types and working of solvers; Exploring through openly available published papers to learn the same.

### References
[[1] Multi-Objective Optimisation Problem](https://en.wikipedia.org/wiki/Multi-objective_optimization)
[[2] Google's OR-Tools](https://developers.google.com/optimization) \
[[3] SCIP Solver](https://scipopt.org/) \
[[4] Slides Briefing on IP solver logics](https://www.dmi.unipg.it/cp2011/downloads/slides/sessions/Tutorial-IntegerProgramming.pdf)
