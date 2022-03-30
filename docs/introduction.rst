Introduction
============

To install ssaw, simply run this command in your terminal::

    $ pip install ssaw

The next step is to import the module and initialize connection with the server::

    import ssaw

    client = ssaw.Client('https://demo.mysurvey.solutions',
        token='your token goes here')

# see https://docs.mysurvey.solutions/headquarters/accounts/token-based-authentication/

Now we're ready to interact with the Survey Solutions server.

Get list of questionnaires::

    for q in ssaw.QuestionnairesApi(client).get_list():
        print(q.title)


Download latest export file in SPSS format::

    from ssaw import ExportApi

    # without export_path parameter file will be saved
    # in the current working directory
    filename = ExportApi(client).get(export_type="SPSS",    
        questionnaire_identity="64136490cbc24a71a1df10f4b7115599$1")


Create new assignment::

    from ssaw.models import Assignment
    from ssaw import AssignmentsApi, QuestionnairesApi
    from ssaw.models import InterviewAnswers

    identifying_data = [
        {"Variable": "address", "Answer": "123 Main Street"},
        {"Variable": "name", "Answer": "Jane Doe"}
    ]
    newobj = Assignment(
        responsible="inter1",
        questionnaire_id="",
        quantity=5,
        identifying_data=identifying_data)

    res = AssignmentsApi(client).create(newobj)
    print(res.id)

    # More advanced example with data-preloading
    q_doc = QuestionnairesApi(client).document(
        id="00000000-0000-0000-0000-000000000000", version=1)

    d = InterviewAnswers(q_doc)
    d.set_answer(variable="address", answer="123 Main Street")
    d.set_answer(variable="name", answer="Jane Doe")
    # question in the first-level roster
    d.set_answer(variable="member_name", answer="Jane", roster_vector=0)
    # second-level roster
    d.set_answer(variable="pet", answer="Cat", roster_vector=[0, 0])

    newobj = Assignment(
        responsible="inter1",
        questionnaire_id="",
        quantity=5,
        identifying_data=d.dict())

    res = AssignmentsApi(client).create(newobj)


Get list of interviews that were updated during last 15 minutes (using GraphQL)::

    import datetime
    from ssaw import InterviewApi

    timestamp = datetime.datetime.now() - datetime.timedelta(minutes=15)
    for i in InterviewsApi(client).get_list(update_date_gt=timestamp):
        print(i)


Get list of map files linked to the interviewer and remove the links::

    from ssaw import MapsApi

    for m in MapsApi(client).get_list(filter_user="inter"):
        print(m.file_name)
        MapsApi(client).delete_user(file_name=m.file_name,
            user_name="inter")


Work with worspaces::

    from ssaw import WorkspacesApi

    # we need to execute workspace commands
    # with administrator credentials
    admin_s = ssaw.Client('https://demo.mysurvey.solutions',
        'admin_user', 'admin_password')

    _ = WorkspacesApi(admin_s).create('new', 'this is a new workspace')
    for w in WorkspacesApi(admin_s).get_list():
        print(w)

    if WorkspacesApi(admin_s).disable('old'):
        print('The old workspace has been disabled')
        print('and is no longer accessible')

