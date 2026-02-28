I copy pasted from the HW04 instructions directly as AI Prompts for creating the lambda functions and pytests.

Namely:
1) Create a python file that should determine the metadata (e.g. filename, file
size, upload date0me, bucket ARN, and eTag) of the file being uploaded
and write that informa0on to the DynamoDB table.

2) Do all the same steps as the first lambda func0on. But name it "hw04-read-fromdynamo" and enable "Func0on URL" with Auth Type of "None".
o This func0on will be invoked via a Lambda Endpoint in the browser.
§ If the URL contains query string parameter of "name", the func0on will
"query" the DynamoDB table by filename.
§ If the URL has no query string, the func0on will do a "Scan" of the
DynamoDB table and return all Items.
§ In both cases, you are to display the full metadata (file_name, file_size,
upload_date0me, bucket_arn, and etag). Use this syntax for the response:
§ Here is an example that shows the JSON format that the lambda should
return:
{
 "items": [
 ... and the rest of the JSON
 ]
}

3) Create pytests that will upload files/objects to S3 and thus
trigger your lambda code.
• Use assert statements in your pytests to check the dynamodb
table contents and the S3 contents to verify that your test did
what you expected it to do.
• Use boto3 in your tests, not MagicMock or any other mock tes0ng
framework.
§ (You do not need to use pylint.)
o Make sure none of the workflows for past homeworks run when you are working
on hw04. Use triggers in all your workflows to accomplish this isola0on! Edit
previous yaml files if needed.
-->This did prompt me to give the name of my other workflows to ensure the criteria was satisfied. I copy pasted what I had from previous workflows to have it check if it should work fine.

Additionally, I realized I made a mistake and forgot to do a git pull at the start of the assignment before merging off of main into feature-hw04. Thus, I didn't have my hw03.yml file in my feature branch. Because of this, I asked a few prompts to make sure I merge things accordingly as I was going through my hw04 workflow checks. It had me to do the following:
git switch feature-hw04 (i noticed i didn't do a git pull when i didn't see my hw03.yml file so i swapped to main)
git merge main
git push