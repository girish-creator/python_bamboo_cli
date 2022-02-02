# Python Atlassian Bamboo CLI Plugin

##Motivation
This plugin was mainly created as I was unable to find a python reference package for sending commands to Atlassian Bamboo server using its CLI.

##Project Description
This is a simple package to use most of the generic Atlassian CLI commands for Bamboo through python functions.

All the functions written in this module are based exactly on the Bamboo Command Line Interface which you can find at the below link:

https://bobswift.atlassian.net/wiki/spaces/BCLI/overview?homepageId=2392068

## Pre-requisites
- Atlassian Command Line Interface should be installed.
- Admin or relatively higher authorization access to the Bamboo server where you want to create your bamboo plans.

## Setup
- Download and Install ACLI for your platform. Use link: 
    - https://bobswift.atlassian.net/wiki/spaces/ACLI/pages/98009238/CLI+Client+Installation+and+Use
- Open the acli.properties files from the installed location and provide the username and password for authenticating to the Bamboo server. 
  In the same file create a variable named "realbamboo" and assign the bamboo server link as a string to this variable. 
  This will be used in the BambooCLI class for connecting to the bamboo server.
  
     - Example:
            realbamboo       = bamboo -s https://server-apps-prd.example.com/ ${credential}

## Usage
Install the python package
> pip install atlassian_bamboo_cli

Import the BambooCLI
> from BambooCLI import BambooActions

Instantiate the BambooCLI class
> bamboo_inst = BambooActions(bamboo_project_name='project_name', 
>                             acli_directory_path='C:\GitHub\python_bamboo_cli\ACLI', 
>                             acli_bamboo_server_name='realbamboo')

Get all plan for a project from Bamboo server
> project_plans = bamboo_inst.get_plan_list()

This will use the project name provided while creating the bamboo instance variable.
