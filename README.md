# A script that interacts with a running web service

A project for Week 2 of 'Automating Real-World Tasks with Python' course.

**Oliver Frolovs, 2020**

This is free and unencumbered software released into the public domain.

## Problem definition

This script reads a bunch of files from a given location, builds JSON requests from them, POSTs the requests to a REST API endpoint and makes sure that the web service responds with success.

## Environment 

The virtual environment is set up in the same fashion as for the first project: `google-cert-python-project-wk1`

## Testing

I've created some test data in `data/feedback` to mimic the data format described in the assignment. This was used for manual testing.

This project is an even stronger candidate for unit testing but I am trying not to make a meal out of small learning projects as I have much more ambitious things in mind.

## Code

The code is written in defensive style, in a sense that it tries to process all possible exceptions meaningfully. Since we are in control of the input files, I do not do much validation of input files, apart from issuing a warning when I think the data file is incomplete.


## Further development

If this were a real project, I'd spend some time on unit tests. If I was also given the code for the web service, the integration testing could have been interesting. I'd probably set up a Travis pipeline for CI.

&mdash; Oliver Frolovs
