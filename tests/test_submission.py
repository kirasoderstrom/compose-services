import uuid
import json

try:
    from  types import SimpleNamespace as SN
except ImportError as error:
    class SN (object):
        def __init__ (self, **kwargs):
            self.__dict__.update(kwargs)
        def __repr__ (self):
            keys = sorted(self.__dict__)
            items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
            return "{}({})".format(type(self).__name__, ", ".join(items))
        def __eq__ (self, other):
            return self.__dict__ == other.__dict__

def test_submission(submission_client):
    assert submission_client, 'should have a configured submission_client'


def test_list_projects(submission_client):
    q = '{ project { id, type, code } }'
    graph = submission_client.query(q)
    assert graph, 'should have a response to graphQL query'
    assert graph['data'], 'should have a data node {}'.format(graph)
    assert graph['data']['project'], 'should have a project(s) node {}'.format(graph)
    projects = list(map(lambda x: SN(**x), graph['data']['project']))
    assert len(projects), 'should have at least one project'
    assert projects[0].type == 'project', 'first element should be a project'
    print(projects)



def test_create_delete_program(submission_client):
    program_name = str(uuid.uuid1())
    program = SN(name=program_name, dbgap_accession_number=program_name, type='program').__dict__
    response = json.loads(submission_client.create_program(program))
    assert 'id' in response, 'could not create program {}'.format(response['message'])
    response = submission_client.delete_program(program_name)
    print('delete response >{}<'.format(response))
    if len(response) == 0:
        response = '{}'
    print('delete response >{}<'.format(json.loads(response)))


def test_delete_program(submission_client):
    program_name = 'smmart'
    print('delete response >{}<'.format(submission_client.delete_program(program_name)))


def create_program(submission_client, program_name):
    program = SN(name=program_name, dbgap_accession_number=program_name, type='program').__dict__
    response = json.loads(submission_client.create_program(program))
    assert 'id' in response, 'could not create program {}'.format(response['message'])
    return response


def create_project(submission_client, program_name, project_name):
    project = SN(name=project_name,
        state="open", availability_type="Open",
        dbgap_accession_number=project_name, code=project_name, type='project').__dict__
    response = json.loads(submission_client.create_project(program_name, project))
    assert response['code']==200 , 'could not create project {}'.format(response['message'])
    return response


def create_node(submission_client, program_name, project_code, node):
    response = json.loads(submission_client.submit_node(program_name, project_code, node))
    assert response['code']==200 , 'could not create {} {}'.format(node['type'], response['message'])
    return response



def create_experiment(submission_client, program_name, project_code, submitter_id):
    experiment = {
        '*projects': {'code': project_code},
        '*submitter_id': submitter_id,
        'type': 'experiment'
    }
    return create_node(submission_client, program_name, project_code, experiment)


def create_case(submission_client, program_name, project_code, submitter_id):
    case = {
        '*experiments': {'submitter_id': project_code},
        '*submitter_id': submitter_id,
        'type': 'case'
    }
    return create_node(submission_client, program_name, project_code, case)


def create_sample(submission_client, program_name, project_code, case_name, submitter_id):
    sample = {
        '*cases': {'submitter_id': case_name},
        '*submitter_id': submitter_id,
        'type': 'sample'
    }
    return create_node(submission_client, program_name, project_code, sample)


def create_aliquot(submission_client, program_name, project_code, sample_name, submitter_id):
    aliquot = {
        '*samples': {'submitter_id': sample_name},
        '*submitter_id': submitter_id,
        'type': 'aliquot'
    }
    return create_node(submission_client, program_name, project_code, aliquot)


def create_submitted_methylation(submission_client, program_name, project_code, aliquot_name, submitter_id):
    submitted_methylation = {
      "*data_category": 'Methylation Data',
      "*data_format": 'IDAT',
      "type": "submitted_methylation",
      "*submitter_id": submitter_id,
      "*data_type": 'Methylation Intensity Values',
      "*md5sum": '12345678901234567890123456789012',
      "*file_size": 1000,
      "aliquots": {
        "submitter_id": aliquot_name
      },
      'urls': 'foo',
      "*file_name": 'my-file-name',
    }
    return create_node(submission_client, program_name, project_code, submitted_methylation)


def test_create_program_project(submission_client):
    program_name = 'smmart'
    project_name = 'atac'
    case_name = 'case-1'
    sample_name = 'sample-1'
    aliquot_name = 'aliquot-1'
    submitted_methylation_name = 'submitted_methylation-1'
    program = create_program(submission_client, program_name)
    project = create_project(submission_client, program_name, project_name)
    experiment = create_experiment(submission_client, program_name, project_name, submitter_id=project_name)
    case = create_case(submission_client, program_name, project_name, submitter_id=case_name)
    sample = create_sample(submission_client, program_name, project_name, case_name, submitter_id=sample_name)
    aliquot = create_aliquot(submission_client, program_name, project_name, sample_name, submitter_id=aliquot_name)
    submitted_methylation = create_submitted_methylation(submission_client, program_name, project_name, aliquot_name, submitter_id=submitted_methylation_name)
    print(submitted_methylation)



def test_query_project(submission_client):
    program_name = 'smmart'
    program = SN(name=program_name, dbgap_accession_number=program_name, type='program').__dict__
    response = json.loads(submission_client.create_program(program))
    assert 'id' in response, 'could not create program {}'.format(response['message'])
    program_id = response['id']
    project_name = 'atac'
    project = SN(name=project_name, dbgap_accession_number=project_name, code=project_name, type='project').__dict__
    response = json.loads(submission_client.create_project(program_name, project))
    print(response)


def test_delete_all_programs(submission_client):
    types = ['submitted_methylation', 'aliquot', 'sample', 'case', 'experiment']
    json.loads(submission_client.delete_node('smmart', 'atac', '9789c4f9-e527-4d9b-854e-dbfca003f25e'))
    for t in types:
        # try:
        print('fetching', t)
        response = submission_client.export_node_all_type("smmart", "atac", t)
        if 'data' not in response:
            print('no data?', response)
        else:
            for n in response['data']:
                print(t, n['node_id'])
                delete_response = json.loads(submission_client.delete_node('smmart', 'atac', n['node_id']))
                assert delete_response['code'] == 200, delete_response
                print('deleted {} {}'.format(t, n['node_id']))
        # except Exception as e:
        #     print('error deleting {} {}'.format(t, str(e)))
        #     raise e
    print(submission_client.delete_project('smmart', 'atac'))
    print(submission_client.delete_program('smmart'))


def test_insert_submitted_file(submission_client):
    id = str(uuid.uuid1())
    print(id)
    response = submission_client.submit_node('smmart', 'atac',
        SN(
            file_name='/home/exacloud/lustre1/adey_lab/share/181127_Jeremy_sciATAC_example_data/03_On_Target.values',
            file_size=338711,
            md5sum='5bc20317dba664ccf666a9f9c7a3c0a0',
            type='submitted_file',
            id=id,
            submitter_id='5bc20317dba664ccf666a9f9c7a3c0a0',
            data_category='misc',
            data_type='misc',
            data_format='misc',
            urls='foo3,bar3',
            projects=[
                {
                  "code": "atac",
                  # "id": "5272d000-f2da-510e-93b3-935d94c9415d"
                }
            ]
            ).__dict__
    )
    print(response)
