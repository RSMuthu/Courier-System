Basic Courier Management System
======================================
This file is used to list changes made in each version of the Basic Courier Management System.

v0.1.1
------
### Bug
- The heap used for vehicle's availability, was shared across instances as it was set as Class attribute. Fixed it to work as object's private attribute.
- The `str` magic method of Product was referring to non-existent discount attribute. Updated it to call the correct method instead.

### Improvements
- Initially, the product selection logic was using brute force method which is not efficient. Altered it to use ILP logic with SCIP solver.
- The complete details of Integer Liner Programming logic is added and explained in the README.
- Added few more additional testcases and addition example for corner case validation.

v0.1.0
------
### Features
- Intelligent Product selection logic for delivery dispatch
- Vehicle management for the delivery transport
- Offer codes & discount management for the delivery products
