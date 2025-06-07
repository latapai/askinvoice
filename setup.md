## Step1: Setup the environment for Resources

#### Option-1
Create the following resources in your IBM Cloud:
- `Storage` --> `Cloud Object Storage`
- `Containers` --> `Code Engine`
- `AI / Machine Learning` --> `Watson Machine Learning`
- `AI / Machine Learning` --> `Watson Assistant`
- `Databases` --> `DB2`

#### Option-2
- Reserve the techzone instance either [Customer Care - GenAI - Option 1](https://techzone.ibm.com/my/reservations/create/64e66590855bcf0017183688) or [Customer Care - GenAI - Option 2](https://techzone.ibm.com/my/reservations/create/64e6866b41bf2a0017d986ad)

## Step2: Setup Project
- In IBM Cloud, under `Resource list`, select the machine learning resource.
- Click launch in `IBM watsonx`
- When in the watsonx console, from the hamburger menu click `View all projects` and create a new project.
- From the project manage tab, associate an machine learning service using the `Services & Integrations` section.

## Step3: Create a DB2 Table
- In IBM Cloud, under `Resource list`, select databases and click on the DB2 database.
- Click `Service Credentials` and create New credentials with the Role as `Manager`. Note down the username, password, host and port.
- Go back to `Manage` and click `Go to UI`.
- Once the UI opens; logout and log back in using copied username and password.
- From the hamburger menu, go to `data` and load the csv data by following the on-screen instructions. Give the table name as `INVOICE_SYNTHETIC`.
- Verify successful load of data by running a select query from the `Run SQL` menu.

## Step4: Create a Code Engine deployment
- In IBM Cloud, under `Resource list`, select Containers and click on the Code Engine container resource.
- Goto `Applications` and click `Create+`.
- Give the application a name, and select `Build container image from source code`.
- Fork the given repository.
- Copy the SSH code from the repository. and paste it under the `Code Repo URL`.
- Click `Specify build details`.
- For SSH secret, if you dont have an SSH key-pair, create a pair and add the public key in the repository settings (under `Deploy Keys`). Add the private key in the while specifying a new SSH secret in build details.
- Enter the branch name as applicable and set context directory to `api` and click Next.
- Set timeout as 4h and set build resource to XL and click Next.
- In `Registry secret` add your IBM IAM Api Key and give some name under the image name. Click Done.
- Set `CPU and memory` to `4 VCPU / 16 GB`. Set `Ephemeral storage (GB)` to `15` and set both min and max number of instances to `1`.
- Under environment variables add all the variables as specified in `example.env` file.
- Under Image start options set `Listening port` to `8000`.
- Click create.
This will start the build run and application deployment. Wait for the deployment to finish.

## Step5: Setup Watson Assistant Chatbot
- In IBM Cloud, under `Resource list`, select the machine learning resource.
- Open the Assistant resource and Launch Watsonx Assistant.
- Follow the initial setup instructions as given on screen.
- From the hamburger menu, open `Integrations` settings. Click `Build custom extension`.
- Follow the on-screen instructions and use the [openapi.json](openapi.json) file from the repo when prompted.
- Go to `Actions`, under `Global Settings` go to `Upload/Download` section and upload the [assistant_action.json](assistant_action.json) file.
- Update any error with the extension (if any). Preview the assistant.
- From the preview page, open `Customize Web Chat` settings. Under the `Embed` settings copy the `integrationID` and `serviceInstanceID`.

## Step6: Deploy UI in Code Engine
- In [index.html](custom_chatbot-main/public/index.html) edit the `integrationID` and `serviceInstanceID` with values from the previous step.
- Update the repository.
- Follow the same steps as `Step4` and change the context directory to `custom_chatbot-main`, give a different image name and set listening port to `3000`.
- Click create and wait for deployment to finish.

Now your chatbot is ready for use. Find the url for the application under `Domain mappings`. Here you can ask your questions about the invoice dataset stored in the DB.