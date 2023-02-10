import boto3
import json

'''
client = boto3.client(
    'emr',
    region_name='us-east-1
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY
)
'''

client = boto3.client(
    'emr',
    region_name = 'us-east-1'
)

response = client.run_job_flow (
    Name='Meu-cluster-emr',
    # version
    ReleaseLabel='emr-6.3.0',
    LogUri='s3://aws-logs-5345324543-us-east-1/elasticmapreduce/',
    Applications=[
        {'Name': 'Hadoop'},
        {'Name': 'Hive'},
        {'Name': 'Spark'}
    ],
    # config das maquinas ec2
    Instances = 
    {
        'InstanceGroups': [
            {
          
                'Name': 'MASTER',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm5.large',
                'InstanceCount': 1,
            }
        ],
        'TerminationProtected': False,
        'Ec2KeyName': 'emr-key',
     },

    BootstrapActions=[
        {
            'Name': 'Download and Extract files on cluster',
            'ScriptBootstrapAction': {
                # bucket S3
                'Path': 's3://stack-app-project-1/app/extract_file.sh'
            }
        },
    ],
    Steps=[
         {
            'Name': 'Run Spark App',
            'ActionOnFailure': 'TERMINATE_CLUSTER',
            # executando comando no cluster
                'HadoopJarStep': {
                    'Args': 
                    ['sudo','spark-submit','/home/hadoop/bancoSpark.py'],
                    'Jar': 'command-runner.jar'
                }
        }
    ],
    VisibleToAllUsers=True,
    ServiceRole = 'EMR_DefaultRole',  
    JobFlowRole = 'EMR_EC2_DefaultRole',
)

print (json.dumps(response, indent=4, sort_keys=True, default=str))