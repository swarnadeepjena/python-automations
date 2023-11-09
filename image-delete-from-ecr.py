import boto3

def get_image_digest(repository_name, image_name, aws_access_key_id, aws_secret_access_key, aws_region):
    # Create an ECR client
    ecr_client = boto3.client('ecr', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Describe images in the repository
    response = ecr_client.describe_images(
        repositoryName=repository_name,
        filter={'tagStatus': 'TAGGED'}  # You may adjust the filter as needed
    )

    # Find the image with the specified name
    for image in response['imageDetails']:
        if 'imageTags' in image and image_name in image['imageTags']:
            return image['imageDigest']

    return None  # Return None if the image with the specified name is not found

def delete_ecr_image(repository_name, image_digest, aws_access_key_id, aws_secret_access_key, aws_region):
    # Create an ECR client
    ecr_client = boto3.client('ecr', region_name=aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    # Specify the repository name and image digest
    image_identifier = {'imageDigest': image_digest}

    # Delete the image
    response = ecr_client.batch_delete_image(
        repositoryName=repository_name,
        imageIds=[image_identifier]
    )

    # Print the response
    print(response)

def delete_ecr_image_by_uri(image_uri, aws_access_key_id, aws_secret_access_key, aws_region):
    # Parse the image URI to extract repository name and image tag
    repository_name, image_tag = image_uri.split('/')[-1].split(':')

    # Get the image digest
    image_digest = get_image_digest(repository_name, image_tag, aws_access_key_id, aws_secret_access_key, aws_region)

    if image_digest:
        # Delete the image using the obtained digest
        delete_ecr_image(repository_name, image_digest, aws_access_key_id, aws_secret_access_key, aws_region)
        print(f"Image '{image_uri}' deleted successfully.")
    else:
        print(f"Image '{image_uri}' not found in the repository.")

# Example usage
image_uri = '***.dkr.ecr.ap-south-1.amazonaws.com/cladma-ml:test-4-latest'
aws_access_key_id = '***'  # Replace 'your-access-key-id' with your AWS access key ID
aws_secret_access_key = '***'  # Replace 'your-secret-access-key' with your AWS secret access key
aws_region = 'ap-south-1'  # Replace 'your-region' with your AWS region

delete_ecr_image_by_uri(image_uri, aws_access_key_id, aws_secret_access_key, aws_region)
