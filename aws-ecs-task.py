#prereq.- install python & boto3

import boto3

ACCESS_KEY='***'
SECRET_KEY='***'


# # Initialize the ECS client
# ecs = boto3.client('ecs')

# Initialize the ECS client with your credentials
ecs = boto3.client('ecs', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY)

# Define your task definition with environment variables
task_definition = {
    'family': 'ml-test-1',  # Replace with your task definition name
    'networkMode': 'awsvpc',
    'requiresCompatibilities': ['FARGATE'],
    'cpu': '1024',
    'memory': '3072',
    'executionRoleArn': 'arn:aws:iam::533163933677:role/ecsTaskExecutionRole',
    'containerDefinitions': [
        {
            'name': 'ml-c-03',
            'image': '533163933677.dkr.ecr.ap-south-1.amazonaws.com/cladma-ml:latest',
            'memory': 3072,
            'cpu': 1024,
            'environment': [  # Add environment variables here
                {
                    'name': 'BUCKET_NAME',
                    'value': 'test-defect-detection',
                },
                {
                    'name': 'JOB_ID',
                    'value': '1',
                },
                {
                    'name': 'INPUT_S3_PREFIX',
                    'value': 'matverse_cladma/basic_defect_detector/1/input/',
                },
                {
                    'name': 'OUTPUT_S3_PREFIX',
                    'value': 'matverse_cladma/basic_defect_detector/1/output/',
                },
                {
                    'name': 'STATUS_S3_PREFIX',
                    'value': 'matverse_cladma/basic_defect_detector/1/status/',
                }
            ],
            'logConfiguration': {  # Add log configuration
                'logDriver': 'awslogs',
                'options': {
                    'awslogs-group': '/ecs/ml-test-2',  # Replace with your Log Group name
                    'awslogs-region': 'ap-south-1',  # Replace with your AWS region
                    'awslogs-stream-prefix': "ecs",  # Replace with a stream prefix
                }
            }
        }
    ],
    }


response = ecs.register_task_definition(**task_definition)
task_definition_arn = response['taskDefinition']['taskDefinitionArn']

# Run a new Fargate task using the task definition
cluster = 'matverse-ml-models-1'  # Replace with your ECS cluster name
launch_type = 'FARGATE'
network_configuration = {
    'awsvpcConfiguration': {
        'subnets': ['subnet-11197978', 'subnet-4f5c9734'],  # Replace with your subnet IDs
        'securityGroups': ['sg-c31928aa'], 
        'assignPublicIp': 'ENABLED', 
    }
}

response = ecs.run_task(
    cluster=cluster,
    launchType=launch_type,
    taskDefinition=task_definition_arn,
    networkConfiguration=network_configuration
)

print("Task ARN:", response['tasks'][0]['taskArn'])
