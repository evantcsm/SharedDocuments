# Share multiple users folders with 1 user
#Create a CSV file with the users that will be shared with the admin user
#Authored by Evan and Julius
#Disclaimer

import sys, httplib2, json, csv;

# For PRODUCTION please use creds.csv
# For TESTING Enter your info:
pressEnter = raw_input("\nPress Enter to login with creds.csv file")
credsCsvFile = open('creds.csv')
csvCreds = csv.reader(credsCsvFile)
csvCredsList = list(csvCreds)

usersInCSV = []
for row in csvCredsList:

    usersInCSV.append(""+''.join(row))

UN1 = usersInCSV[0]
PW1 = usersInCSV[1]
IK1 = usersInCSV[2]

username = UN1
password = PW1
integratorKey = IK1

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
print loginInfo

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

adminUser= raw_input("\nEnter the UserId that is gaining access to multiple user's folders: ")

csvFile = raw_input("\nEnter CSV Filename (include .csv to name): ")

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
#fileContents = open("test_doc.txt", "r").read();

requestBody = envelopeDef;

#print requestBody;

# append "/envelopes" to the baseUrl and use in the request
url = baseUrl + "/shared_access";
headers = {'X-DocuSign-Authentication': authenticateStr, 'Content-Type': 'application/json', 'Accept': 'application/json'};
http = httplib2.Http();
response, content = http.request(url, 'PUT', headers=headers, body=requestBody);
status = response.get('status');
if (status != '200'):
    print("Error calling webservice, status is: %s\nError description - %s" % (status, content)); sys.exit();
data = json.loads(content);
#envId = data.get('envelopeId');
print content
#--- display results
print ("\nUsers updated!");
