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

Brute force logic is used here to check the combinations.\
This is more of Mixed-integer optimization problem (multi-objective multi-bin knapsack problem) \
After explorations, Google's OR-Tools (or any other MIP solver) is best suited to solve these kind of problems, considering the time and space complexity we might face with huge dataset

### Application Useage
This is a command line based application with `poetry` as package manager.\
There are two poetry scripts to trigger the application

> `$ poetry run courier`

 Triggers the application and lets the user input the information. As the user provides the data, it will validated immediately and then, the courier delivery gets triggered

 > `$ poetry run courier-cli -f "examples/sample1.json"`

Triggers the application but instead of giving control to user, the necessary data is fed via json file.\
The validation happens over the data loaded from the json file and then the courier delivery triggers

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
- Package/Product selection logic is set to brute-force for now. It needs to be updated with MIP solver with model based resolution. \
Although I used this time to explore little on this Mixed Integer Problem and OR-Tools, the solution is not added in this application currently as I have tried it enough myself.
- The available Offer details are stored as Config for now. This needs to be updated to use database that way, the data management would be easier and the Offer related data would persist in DB. Ofcourse, this will very much matter when application scales up.
- The `dockerfile` can also be cleaned (add another stage to split the application working from the `python-base`) & updated with the security aspects & the Entry point can also be setup with `tini` (or something similar).

### Learning Takeaways
While working on this, most time I spent was on reading through Mixed Integer Programming, Constraint Programming and few other concepts of optimization problem. \
Althought I am still a beginner in this field, I just got curious and exploring in my free time. And also as I am just started to try it, I have not added optimization solution into this code base. I had a good learn on this interesting things.
