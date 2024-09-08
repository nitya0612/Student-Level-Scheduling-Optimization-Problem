Hybrid Timetable Scheduling Optimization

Overview

This repository contains the implementation of a Hybrid Timetable Scheduling Optimization for MSBA students at Warwick Business School (WBS). The problem is based on the mixed-integer programming approach proposed by Moallemi and Patange (2023). The focus is on optimizing student-level schedules for six main MSBA modules under the assumption that all classes are scheduled in person.

Key Objectives:
Problem Formulation: Provide a clear explanation of the scheduling optimization, including decision variables, constraints, objective function, and required parameters.
Data Preparation: Utilize provided datasets and any additional information to prepare the necessary data for the optimization.
Optimization: Implement and solve the optimization problem in Python, analyzing various solutions by adjusting parameters.
Recommendations: Suggest improvements or alternative implementations for the proposed formulation.
Problem Description

The goal is to create an efficient schedule that minimizes scheduling conflicts and meets various constraints such as room capacity, student preferences, and course availability.
The optimization is formulated as a Mixed-Integer Programming (MIP) problem.
Key Components:
Decision Variables: Variables that determine whether a student is assigned to a class at a particular time.
Constraints: Constraints include room capacity, module availability, student enrollment, and time slot preferences.
Objective Function: Minimize conflicts and maximize scheduling efficiency while adhering to the constraints.
