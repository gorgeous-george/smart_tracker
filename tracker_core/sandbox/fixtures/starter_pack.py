from dashboard.models import CoreObject, Dataset

def starter_datasets(request):
    d = Dataset.objects.bulk_create([
        Dataset(dataset="SUPPLIES",
                description="Important resources,food, water, other staff",
                owner=request.user),
        Dataset(dataset="UTILITIES",
                description="Paid services, regular payments",
                owner=request.user),
        Dataset(dataset="HOME ROUTINE",
                description="Cleaning, other home tasks",
                owner=request.user),
        Dataset(dataset="DAY ROUTINE",
                description="Development of habits that make impact",
                owner=request.user),
        Dataset(dataset="MONTHLY TASK",
                description="Valuable goals to be achieved",
                owner=request.user),
    ])

def starter_objects(request):
    c = CoreObject.objects.bulk_create([
        CoreObject(name="Water",
                   description="Clear drinking water",
                   dataset_id=Dataset.objects.get(dataset="SUPPLIES").id,
                   current_value="Green",
                   priority="High",
                   measure_description="G-Fully supplied, O-Running low, R-Run out of",
                   status="Green",
                   timeframe="Week",
                   responsible=request.user,
                   ),
        CoreObject(name="Food",
                   description="Vegetables, fruits, meat, eggs, milk+, coffee, tea",
                   dataset_id=Dataset.objects.get(dataset="SUPPLIES").id,
                   current_value="Green",
                   priority="Moderate",
                   measure_description="G-Fully supplied, O-Running low, R-Run out of",
                   status="Green",
                   timeframe="Week",
                   responsible=request.user,
                   ),
        CoreObject(name="Cleaning",
                   description="Making home clean",
                   dataset_id=Dataset.objects.get(dataset="HOME ROUTINE").id,
                   current_value="Green",
                   priority="Moderate",
                   measure_description="G-Cleanliness, O-Some disorder, R-Mess",
                   status="Green",
                   timeframe="Week",
                   responsible=request.user,
                   ),
        CoreObject(name="Home Comfort",
                   description="Making home cozy and comfort place to live",
                   dataset_id=Dataset.objects.get(dataset="HOME ROUTINE").id,
                   current_value="Green",
                   priority="Moderate",
                   measure_description="G-Hygge, O-Neutral atmosphere, R-Unpleasant",
                   status="Green",
                   timeframe="Week",
                   responsible=request.user,
                   ),
        CoreObject(name="Family Day",
                   description="Meet with family",
                   dataset_id=Dataset.objects.get(dataset="MONTHLY TASK").id,
                   current_value="Green",
                   priority="High",
                   measure_description="G-Met this month, O-Meeting is arranged, R-Not met",
                   status="Green",
                   timeframe="Month",
                   responsible=request.user,
                   ),
        CoreObject(name="Job Search",
                   description="Search of vacancies, applying, moving things further",
                   dataset_id=Dataset.objects.get(dataset="MONTHLY TASK").id,
                   current_value="Green",
                   priority="High",
                   measure_description="G-Performing tests/interview, O-Proactively searching, R-Not searched",
                   status="Green",
                   timeframe="Month",
                   responsible=request.user,
                   ),
        CoreObject(name="Physical Training",
                   description="Morning exercises, gymnastic, stretching, outdoor activity",
                   dataset_id=Dataset.objects.get(dataset="DAY ROUTINE").id,
                   current_value="Green",
                   priority="High",
                   measure_description="G-Performed today, O-Skipped one day, R-Skipped two days",
                   status="Green",
                   timeframe="Day",
                   responsible=request.user,
                   ),
        CoreObject(name="Programming",
                   description="Learning Python, improving developing skills",
                   dataset_id=Dataset.objects.get(dataset="DAY ROUTINE").id,
                   current_value="Green",
                   priority="High",
                   measure_description="G-Performed today, O-Skipped one day, R-Skipped two days",
                   status="Green",
                   timeframe="Day",
                   responsible=request.user,
                   ),
        CoreObject(name="Menthal Health",
                   description="Mediation, practices, therapy",
                   dataset_id=Dataset.objects.get(dataset="DAY ROUTINE").id,
                   current_value="Green",
                   priority="High",
                   measure_description="G-Performed today, O-Skipped one day, R-Skipped two days",
                   status="Green",
                   timeframe="Day",
                   responsible=request.user,
                   ),
        CoreObject(name="Pay apartment bills",
                   description="Pay rent and utility bills",
                   dataset_id=Dataset.objects.get(dataset="UTILITIES").id,
                   current_value="Green",
                   priority="High",
                   measure_description="G-Paid, O-Bill is received, R-DEBT",
                   status="Green",
                   timeframe="Month",
                   responsible=request.user,
                   ),
        CoreObject(name="Pay regular bills",
                   description="Pay Golan, Lifecell, Luckynet",
                   dataset_id=Dataset.objects.get(dataset="UTILITIES").id,
                   current_value="Green",
                   priority="High",
                   measure_description="G-Paid, O-Bill is received, R-DEBT",
                   status="Green",
                   timeframe="Month",
                   responsible=request.user,
                   ),
    ])
