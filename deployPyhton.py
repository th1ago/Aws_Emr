"""
Copy paste the following code in your Lambda function. Make sure to change the following key parameters for the API as per your account

-Name (Name of Spark cluster)
-LogUri (S3 bucket to store EMR logs)
-Ec2SubnetId (The subnet to launch the cluster into)
-JobFlowRole (Service role for EC2)
-ServiceRole (Service role for Amazon EMR)

The following parameters are additional parameters for the Spark job itself. Change the bucket name and prefix for the Spark job (located at the bottom).

-s3://your-bucket-name/prefix/lambda-emr/SparkProfitCalc.jar (Spark jar file)
-s3://your-bucket-name/prefix/fake_sales_data.csv (Input data file in S3)
-s3://your-bucket-name/prefix/outputs/report_1/ (Output location in S3)
"""
import json
import boto3

client = boto3.client('emr')

def lambda_handler(event, context):

    response = client.run_job_flow(
        Name = 'spark_job_cluester',
        LogUri = 's3://aws-logs-098133264264-us-east-1/prefix/logs',
        ReleaseLabel = 'emr-6.9.0',
        Instances={
            'MasterInstanceType': 'm5.xlarge',
            'SlaveInstanceType': 'm5.large',
            'InstanceCount': 1,
            'KeepJobFlowAliveWhenNoSteps': False,
            'TerminationProtected': False
        },
        Applications=[
            {'Name': 'Hadoop'},
            {'Name': 'Hive'},
            {'Name': 'Spark'}
        ],
        Configurations = [
            { 'Classification': 'spark-hive-site',
              'Properties': {
                  'hive.metastore.client.factory.class': 'com.amazonaws.glue.catalog.metastore.AWSGlueDataCatalogHiveClientFactory'}
            }
        ],
        VisibleToAllUsers=True,
        JobFlowRole = 'EMR_EC2_DefaultRole',
        ServiceRole = 'EMR_DefaultRole',
        Steps = [
            {
                'Name': 'flow-log-analysis',
                'ActionOnFailure': 'TERMINATE_CLUSTER',
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': [
                        'spark-submit',
                        '--deploy-mode', 'cluster',
                        '--executor-memory', '6G',
                        '--num-executors', '1',
                        '--executor-cores', '2',
                        '--class', 'com.aws.emr.ProfitCalc',
                        's3://aws-logs-098133264264-us-east-1/prefix/lambda-emr/SparkProfitCalc.jar',
                        's3://aws-logs-098133264264-us-east-1/prefix/fake_sales_data.csv',
                        's3://aws-logs-098133264264-us-east-1/prefix/outputs/report_1/'
                    ]
                }
            }
        ]
    )