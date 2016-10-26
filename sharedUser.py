# Share multiple users folders with 1 user
#Create a CSV file with the users that will be shared with the admin user
#Authored by Evan and Julius
#Disclaimer

import sys, httplib2, json, csv;

print ("\n*******************************"
       '\n*      TCSM Tool Kit          *'
       '\n*         beta 1.0            *'
       '\n*******************************')

# For PRODUCTION please use creds.csv
# For TESTING Enter your info:
pressEnter = raw_input("\nPress Enter to login with creds.csv file")
credsCsvFile = open('creds.csv')
csvCreds = csv.reader(credsCsvFile)
csvCredsList = list(csvCreds)

usersInCSV = []
for row in csvCredsList:

    usersInCSV.append(""+''.join(row))

username = usersInCSV[0]
password = usersInCSV[1]
integratorKey = usersInCSV[2]

authenticateStr = "<DocuSignCredentials>" \
                    "<Username>" + username + "</Username>" \
                    "<Password>" + password + "</Password>" \
                    "<IntegratorKey>" + integratorKey + "</IntegratorKey>" \
                    "</DocuSignCredentials>";

#
# STEP 1 - Login
#
url = 'https://demo.docusign.net/restapi/v2/login_information';
headers = {'X-DocuSign-Authentication': authenticateStr, 'Accept': 'application/json'};
http = httplib2.Http();
response, content = http.request(url, 'GET', headers=headers);

status = response.get('status');
if (status != '200'):
    print("Error calling webservice, status is: %s" % status); sys.exit();

# get the baseUrl and accountId from the response body
data = json.loads(content);
loginInfo = data.get('loginAccounts');
D = loginInfo[0];
baseUrl = D['baseUrl'];
accountId = D['accountId'];
#print loginInfo

#--- display results
print ("baseUrl = %s\naccountId = %s" % (baseUrl, accountId));

#
# STEP 2 - Add the admin user Id and the csv file of the users you are sharing
#

print ('\nWhat would you like to do?\n'
                     '\n[1] Share To'
                     '\n[2] Share From'
                     '\n[3] Remove Sharing')

multi = int(raw_input("\nPlease enter your selection: "))

sharedOption = ""

if multi == 1:
    sharedOption = 'shared_to'
elif multi== 2:
    sharedOption = 'shared_from'
elif multi== 3:
    sharedOption = 'not_shared'
else:
    print"\nInvalid Choice"
    print ('\nWhat would you like to do?\n'
                         '\n[1] Share To'
                         '\n[2] Share From'
                         '\n[3] Remove Sharing')
    int(raw_input("\nPlease enter your selection: "))

#print sharedOption

adminUserInput = raw_input("\nEnter the UserId that is gaining access to multiple user's folders: ")

if len(adminUserInput) == 36:
    adminUser = adminUserInput


else:
    print "\nInvalid UserId. Guid should contain 32 digits with 4 dashes (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)"
    adminUserInput = raw_input("\nEnter the UserId that is gaining access to multiple user's folders: ")

    if len(adminUserInput) == 36:
        adminUser = adminUserInput

    else:
        sys.exit()


pressEnter = raw_input("\nPress Enter to modify users in the users.csv file")

csvFile = 'users.csv'
f = open(csvFile)
csv_f = csv.reader(f)
csv_list = list(csv_f)
First = "{\"user\":{""\"userId\":\""
Last = "\"},\"shared\":\"" + sharedOption + "\"},"

listData = []
for row in csv_list:

    listData.append(First +'' .join(row) + Last)

newData = "" +''.join(listData);

#uncomment newData to see users passed in API call
#print newData



#construct the body of the request in JSON format
envelopeDef =   "{\"sharedAccess\":[{" + \
                "\"user\":{" + \
                "\"userId\":\"" + \
                adminUser + \
                "\"}," + \
                "\"envelopes\":[" + \
                newData + \
                "]}]}";

# convert the file into a string and add to the request body

requestBody = envelopeDef;

# append "/envelopes" to the baseUrl and use in the request
url = baseUrl + "/shared_access";
headers = {'X-DocuSign-Authentication': authenticateStr, 'Content-Type': 'application/json', 'Accept': 'application/json'};
http = httplib2.Http();
response, content = http.request(url, 'PUT', headers=headers, body=requestBody);
status = response.get('status');
if (status != '200'):
    print("Error calling webservice, status is: %s\nError description - %s" % (status, content)); sys.exit();
data = json.loads(content);

print "\nAPI Response: \n"
print content

#--- display results
print ("\nUsers updated!");
