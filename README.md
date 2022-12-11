# Cadmus
Automatic Zoom meeting follow-up for engineering managers and architects

This is the project for [$50K Assembly AI Hackathon](https://hopin.com/events/assemblyai-ai-hackathon).

## [Devpost project link](https://devpost.com/software/tbd-jde4tr)


# Project Story
## What Inspired Us
As engineering managers and architects, we found ourselves spending a significant amount of time in meetings - on average, 9 hours per week. This time could have been better spent on more productive tasks, but we also realized that we were missing out on key information and insights from these meetings.

That's what inspired us to create the Cadmus project - an automatic follow-up app for Zoom meetings that provides a concise summary of the meeting, highlighting important agreements, potential risks, and valuable insights.

## What We Learned
As we started working on the Cadmus project, we quickly realized the challenges involved in extracting relevant information from meetings and summarizing them in a way that is easy to understand.

We also learned about the latest technologies in the field, such as Google Cloud AI and OpenAI, which allowed us to support 190 languages and accurately summarize meetings in a fraction of the time they would normally take.

## How We Built the Project
Building the Cadmus project was a challenging but rewarding process. We started by researching the latest technologies and algorithms in the field of natural language processing and automatic summarization.

Next, we designed and implemented the core functionality of the app, which involved uploading Zoom meetings, processing the audio and transcript, and generating a summary.

Throughout the development process, we faced several challenges, such as dealing with different accents and dialects, but we were able to overcome these challenges through careful testing and optimization.

## Challenges We Faced
One of the biggest challenges we faced was accurately summarizing meetings with a high degree of accuracy. This involved dealing with different accents, dialects, and speaking styles, as well as ensuring that the summary captured the key points of the meeting without losing important details.

Another challenge was the cost of processing meetings. We wanted to keep the cost per hour of a meeting as low as possible, which required careful optimization of our algorithms and the use of efficient technologies such as Google Cloud AI and OpenAI.

Overall, the Cadmus project was a challenging but rewarding experience, and we are proud of the results we have achieved so far.

Finally, our MVP can accurately extract from the audio transcript summary, insights, arrangements and even risks.

## Screenshots
![Alt text](https://user-images.githubusercontent.com/5506168/206925662-46788a3e-28fa-4ec8-8c16-694412000c13.png "1")
![Alt text](https://user-images.githubusercontent.com/5506168/206925665-3742db4b-6c1c-425e-9280-81745b6916ff.png "2")
![Alt text](https://user-images.githubusercontent.com/5506168/206925670-205af6d7-0dbb-453b-aa09-8ff3b5eae8f2.png "3")

## How to use
0. To use this app you have to pass your API KEYS TO GCP and Open AI:
```
export OPENAI_API_KEY="your_openai_key"; 
export GOOGLE_APPLICATION_CREDENTIALS="my-project-98575-371210-114ac428d015.json"; # path to you cred file
```
1. Start flask application ```python3 app.py```
2. Upload Zoom video using the form
3. Wait for the result and check Summary, Insights, Risks, Arrangements and Transcript
