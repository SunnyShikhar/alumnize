# Alumnize: Alumni Intelligence System - User Guide 

Documentation instructing how to use alumnize to gather, transform and analyze alumni data for the University of Waterloo Capstone Project.

<b> Website: </b> https://alumnize-capstone.herokuapp.com/

Table of Contents
-----------------

  * [Prerequisites](#prerequsites)
  * [Gather Data](#gather-data)
  * [Transform Data](#transform-data)
  * [Analyze Data](#analyze-data)
  * [Additional Information](#additional-information)
     * [Transformation Logic](#transformation-logic)
     * [Limitations](#limitations)

## Prerequisites

Please ensure the following programs are downloaded and installed to use Alumnize:

- [Google Chrome](https://www.google.ca/chrome/ "Download Google Chrome")
- [Alumni Data Buddy Chrome Extension](https://chrome.google.com/webstore/detail/alumni-data-buddy/mofobkcfdkiejnmffkoldjlflldddjpb/ "Download Alumni Data Buddy")
- [Tableau Education License](https://www.tableau.com/academic/students "Downlad Tableau Education License")

## Gather Data

1. Go to a LinkedIn profile of an alumnus.

2. Click the download button that appears in the header when Alumni Data Buddy Chrome Extension is enabled.

![Figure1](https://github.com/SunnyShikhar/alumnize/blob/master/almabase/static/img/linkedIn.png?raw=true)

3. Repeat for 50 profiles (limitation set by the Chrome extension).

4. Click the chrome extension beside the URL bar.

![Figure2](https://github.com/SunnyShikhar/alumnize/blob/master/almabase/static/img/url.png?raw=true)
      
5. Enter e-mail and download.

![Figure3](https://github.com/SunnyShikhar/alumnize/blob/master/almabase/static/img/almabase.png?raw=true)

Repeat this process until all alumni profiles have been downloaded.

## Transform Data 

1. Go to [Alumnize](https://alumnize-capstone.herokuapp.com/ "Alumnize Home Page")

![Figure4](https://github.com/SunnyShikhar/alumnize/blob/master/almabase/static/img/alumnize.png?raw=true)

2. Upload the almabase output file(s) exported using the extension.

3.1 If this is the first time using the website, there is no need to upload a master file.

3.2 If this is not the first time, please upload the latest file outputted from Alumnize ('MasterFile.csv').

4. Click Transform.

5. Save the output file.

## Analyze Data

- Tableau Instructions

## Additional Information

### Transformation Logic

The following is a brief explanation of how the fields within the transformed dataset are determined.

<b> ID: </b> Identifier that is unique for each person in the dataset

<b> Work ID/Coop ID: </b> The Work ID is a unique identifier for each person for each job that is a full-time position. Coop ID is for coop positions. These fields are determined using the graduating year. If the graduating year is before the start month-year of a position, the work ID column is populated; else, the coop
ID column is populated. 

<b> Name: </b> Obtained from the “Name” column in the data extracted from Almabase

<b> Year: </b> Determined by looking at the education duration for any education done in Waterloo. Looks for “waterloo” as education location in the two most recent educations, starting with the 2nd most recent. If the 2nd most recent education is Waterloo, it’s duration-end is used as education year and it is assumed that the most recent education is a post-graduate education. Otherwise, if the most-recent education location is “waterloo”, similar steps are taken.

<b> Company: </b> Determined from the “Employment: Employer 1” column in the data extracted from Almabase. Same is done for Employer two to five if the person has multiple employments on their LinkedIn profile.

<b> Position: </b> Determined from the “Employment: Title 1” column in the data extracted from Almabase. Same is done for Title two to five if the person has multiple employments on their LinkedIn profile.

<b> URL: </b> Determined from the “LinkedIn URL” column in the data extracted from Almabase. The same URL is used for multiple rows in which multiple employments of the same person are present.

<b> All Date fields: </b> Job position durations can be inputted in various formats by users. Rule-based logic was created to account for all cases of duration in job positions represented by the “date_format” function in the transform script which takes the raw duration as input from the Almabase file. The different formats are:

* Month Year – Month Year
* Year – Year
* Month Year – Year
* Year – Month Year
* Month Year – Present (current job)
* Year – Present (current job)

The following columns are created within the transformed dataset:
* Duration – Full Dates of job duration including mm/yyyy-mm/yyyy OR yyyy-yyyy
* Start.Date – Start date including mm/yyyy or yyyy
* Start.Month
* Start.Year
* End.Date.pres - End date including mm/yyyy OR yyyy OR pres for current positions
* End.Month
* End.Year
* Job.Duration – Total job duration in years (Ex. 0.2 years)

<b> Full.Location: </b> Raw location obtained from data extracted from Almabase

<b> City & Country: </b> The content in the location attribute from LinkedIn is inconsistent. Toronto could be entered as "Toronto, ON" or "Toronto, Ontario, Canada", "GTA" or " Toronto". This deemed to be problematic when conducting location analysis of alumni jobs. Initially, string-based rules were considered to standardize the city and country from locations, however it is impossible to account for different cases for thousands of cities around the world. Instead, this issue was handled by implementing the external Python libraries Geopy and Geotext. Geopy leverages Google Maps API to extract the full address of the location attribute. Geotext then extracts city and country from the full address. 

Despite efforts to extract and standardize the location attribute, Geopy has certain limitations due to Google Maps API. Google Maps API limits the free service to 2500 requests per day, calculated as a sum of client-side and server-side queries. Thus, requests for only 1,250 locations can be accepted by the API daily. If there are five job positions per alumni, a maximum of 250 alumni profiles can be transformed per day. If the user exceeds the maximum allowed requests, Geotext is used to extract the city and country from the
location attribute. This method is less accurate than using the combination of Geopy and Geotext.

<b> Append/Replace Functionality within Transformation Script </b>

The user may have a Masterfile of all of the previously extracted and transformed alumni. If transformation is applied on newly extracted data, the user can append/replace the data in the current Masterfile as long as a path to the Masterfile is added. Otherwise, the newly extracted data will be transformed only without append/replace into another csv. If the user inputs a file path for a Masterfile and an almabase output, the transform_script.py will append new and replace old rows in the Masterfile. A unique identifier for a row is the combination of “Name”, “Year”, “Company”, and “Position”. The append_replace() method in the script implements the following steps:

* Inserts all primary keys (“Name” + “Year” + “Company” + “Position”) of the Masterfile into a dictionary
* Inserts all primary keys (“Name” + “Year” + “Company” + “Position”) of the newly transformed almabase output into a dictionary
* Using the two dictionaries, it finds any new primary keys present in the newly transformed almabase output and not in Masterfile
* The script appends all new rows to the Masterfile as well as replace old rows present in the Masterfile and newly transformed almabase output.

There are a few limitations with the append_replace() method. One limitation is that it cannot handle duplicate “Name” and “Year” combination. For example, if there are two alumni named “John Smith” from the class of 2012 present in the Masterfile under “ID”s 1 and 2, the new rows that are appended to the Masterfile may be appended under the incorrect “ID”. However, for the current Management Engineering dataset, no alumni has the same “Name” and “Year” combination. Furthermore, if any of the alumni change their “Name”, “Year”, “Company” and/or “Position” on LinkedIn for an old data point in the Masterfile, a duplicate row will be appended to the Masterfile (as the primary key has changed).

### Limitations

At the moment the website is only ablet to handle small data that takes less than 30 seconds to compute. This limitation will soon be resolved.