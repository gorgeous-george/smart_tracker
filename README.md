# Hello stranger! Here is a SMART tracker of any thing

SMART Tracker engine provides user with the following features:
1. Create, edit, delete the datasets containing objects/tasks/goals/resources.
2. Monitor the fulfillment/availability of the objects by descriptive dashboard, filters, and interactive chart.
3. Receive email notifications and summary reports (currently in development)

Additional features:
- Authentication/Authorization
- User permissions (currently in development)
- API returning datasets/objects (currently in development)
- Admin tools (Flower, Pgadmin) (currently in development)


## App description

- The SMART stands for Specific, Measurable, Achievable, Relevant, and Time-Bound. Defining these parameters as they 
pertain to your goal helps ensure that your objectives are attainable within a certain time frame.

- By default, we provide you with starter pack of resources/tasks you need to keep eye on to have your house/apartment 
supplied, cleaned and paid. Each status is monitored and represented by chart.

- You can start with pre-defined datasets, or create your own! Feel free to use our SMART engine to track literally 
any thing.

## Common logic

- User receives a short tutorial describing SMART concept and main application modules: SANDBOX and DASHBOARD.
- SANDBOX is used to create/edit/delete datasets and related objects. 
- Each object can be related only to one dataset.
- Each object has list of settings required by SMART concept (current value, priority, measure, time frame, responsible).
- Each object would have one of three statuses based on simple pattern "Red-Orange-Green". This can be interpreted as 
"Absent-Running low-Available" or "Not done-In process-Performed" and so on. Each object has its own level of priority 
and current value set by user, so that application defines status of the object comparing current value with the priority.
- DASHBOARD is used to see the current status of the objects, data table, chart. It also provides interactive filters 
by dataset, status, priority and timeframe.

## Architecture

- Docker-Compose
- Django server
- Django REST
- PostgreSQL

## Quick start

TBD