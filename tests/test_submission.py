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




def test_create_program_project(submission_client):
    program_name = 'smmart'
    program = SN(name=program_name, dbgap_accession_number=program_name, type='program').__dict__
    response = json.loads(submission_client.create_program(program))
    assert 'id' in response, 'could not create program {}'.format(response['message'])
    program_id = response['id']
    project_name = 'atac'
    project = SN(name=project_name,
        state="open", availability_type="Open",
        dbgap_accession_number=project_name, code=project_name, type='project').__dict__
    response = json.loads(submission_client.create_project(program_name, project))
    print(response)



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
