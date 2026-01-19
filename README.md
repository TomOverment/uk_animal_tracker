# Mammal Tracking README

## Fictional Client Brief

### Client: UK Nature Connect (fictional public engagement and conservation organisation)

Background
UK Nature Connect works to increase public engagement with wildlife and nature across the United Kingdom. The organisation collaborates with educators, local councils, and conservation groups to make biodiversity data accessible and meaningful to non-technical audiences.

The client has access to the National Mammal Atlas Project dataset, which contains large volumes of citizen-science mammal observation records. However, the dataset is currently under-utilised by the general public due to its size and technical complexity.

Client Objectives

Increase public interest and engagement with UK mammals.

Make complex biodiversity data intuitive and interactive.

Encourage people to explore nature locally and notice wildlife in their surroundings.

Support long-term conservation awareness through data-driven storytelling.

Client Requirements
The client requests a public-facing interactive dashboard that:

Visualises mammal observation data clearly and engagingly.

Allows users to explore species, locations, and time trends.

Goes beyond static visualisation by offering predictive or forward-looking insights.

Is suitable for use by non-technical users (e.g. families, schools, community groups).

My Response / Proposed Solution

Proposed Approach
To meet the client’s objectives, I propose developing an AI-enhanced interactive dashboard that combines historical data visualisation with a predictive machine-learning model.

The solution will not only show where mammals have been observed, but will also estimate the probability of future mammal sightings by location and time, encouraging users to engage with nature proactively.

1. Dashboard Concept

The dashboard will include:

An interactive map showing historical mammal observations.

Filters for species, year, and region.

Time-series charts illustrating trends in mammal reporting.

Educational annotations explaining patterns and seasonal behaviour.

This supports data storytelling, making the dataset approachable and engaging for the public.

2. AI Model: Predicting Future Mammal Sightings

To add value beyond standard visualisation, an AI model will be developed to estimate the probability of mammal presence at a given location and time.

Model Objective
Predict the likelihood of a mammal observation based on:

Geographic location (latitude, longitude)

Time features (year, month, season)

Species or taxonomic group

Historical observation density

Intended User Experience

A user selects a species and a time window (e.g. “Spring”).

The dashboard highlights areas where sightings are more likely based on historical patterns.

The model output is presented as probabilities or heat-maps, not definitive predictions, to avoid misinterpretation.

3. Responsible Use of AI

The model will be positioned as a probability-based engagement tool, not a precise wildlife tracker.

Key considerations:

Predictions reflect historical reporting patterns, not guaranteed animal presence.

Results are influenced by observer effort and reporting bias.

Clear disclaimers will explain that outputs are indicative and educational.

This aligns with ethical AI use and conservation best practices.

4. Value to the Client

This solution:

Transforms static biodiversity records into an interactive public experience.

Encourages people to explore nature locally.

Uses AI to create curiosity and engagement rather than passive consumption.

Demonstrates innovative, responsible use of data science for environmental awareness.

One-Sentence Summary (Excellent for Assessment)

This project responds to a fictional client brief by transforming UK mammal observation data into an AI-enhanced dashboard that both visualises historical trends and predicts the probability of future mammal sightings to engage the public with nature.

User Stories and Acceptance Criteria

Project: UK Mammal Engagement Dashboard
Client: UK Nature Connect (fictional)

The project is guided by user stories focused on public engagement, education,
and responsible AI usage. Acceptance criteria ensure that the dashboard remains
accessible to non-technical users while demonstrating advanced data analytics
and AI techniques aligned with the client’s engagement goals.


User Story 1 – Explore Mammal Sightings Visually

As a member of the public interested in nature
I want to view mammal sightings on an interactive map
So that I can understand where mammals have been observed across the UK.

Acceptance Criteria

The dashboard displays a map of the UK with mammal observation points.

Users can zoom and pan the map.

Hovering over a point shows key information (species name, year, location).

The map loads within a reasonable time despite the large dataset.

The visualisation is understandable to non-technical users.

User Story 2 – Filter Data by Time and Species

As a curious user or educator
I want to filter mammal data by year and species
So that I can explore trends and patterns over time.

Acceptance Criteria

Users can select a year or range of years using a slider or dropdown.

Users can select a species (or view all species).

Charts and maps update dynamically when filters are applied.

Only years present in the dataset are shown (no empty or misleading years).

Filter selections are clearly labelled and easy to reset.

User Story 3 – Understand Trends in Mammal Recording

As a user interested in wildlife trends
I want to see how mammal records change over time
So that I can understand increases or decreases in reporting activity.

Acceptance Criteria

A time-series chart shows the number of records per year.

The chart reflects only valid years from the dataset.

Partial years (e.g. the most recent year) are clearly indicated or explained.

The chart includes titles and axis labels suitable for a public audience.

A short explanatory text accompanies the chart.

User Story 4 – Engage with Predictive Insights (AI Feature)

As a user interested in future wildlife encounters
I want to see the probability of mammal sightings by location and time
So that I can be encouraged to explore nature in my local area.

Acceptance Criteria

The dashboard includes an AI-driven feature that estimates sighting probability.

Users can select:

a species (or group),

a time period (e.g. month or season).

The output is presented visually (e.g. heatmap or probability shading).

Predictions are clearly labelled as probabilities, not guarantees.

The model uses historical observation patterns as input features.

User Story 5 – Understand AI Limitations and Data Bias

As a responsible user
I want clear explanations of how predictions are generated
So that I do not misinterpret AI outputs as exact wildlife locations.

Acceptance Criteria

The dashboard includes a section explaining how the AI model works at a high level.

Limitations such as reporting bias and uneven geographic coverage are stated.

Users are informed that predictions reflect historical data, not real-time tracking.

Language is accessible and avoids technical jargon where possible.

Ethical considerations are clearly acknowledged.

User Story 6 – Educational Use and Storytelling

As an educator or community organiser
I want the dashboard to tell a clear story using data
So that it can be used to engage learners with biodiversity and conservation.

Acceptance Criteria

Visualisations are accompanied by short explanatory text.

Key insights (e.g. most recorded species, seasonal trends) are highlighted.

The dashboard avoids overwhelming users with excessive controls.

The content is suitable for a non-specialist audience.

The dashboard supports exploration rather than static viewing.

User Story 7 – Technical Transparency (Assessment-Focused)

As a project assessor or technical reviewer
I want to see evidence of structured data analysis and AI usage
So that the project demonstrates applied data analytics skills.

Acceptance Criteria

A Jupyter Notebook documents data loading, cleaning, EDA, and evaluation.

AI usage is explicitly described in the notebook and README.

Visualisations in the dashboard are consistent with notebook findings.

The project structure separates analysis (notebook) from presentation (dashboard).

Code is reproducible and well organised.
## Deployment Reminders

* Set the `.python-version` Python version to a [Heroku-22](https://devcenter.heroku.com/articles/python-support#supported-runtimes) stack currently supported version that closest matches what you used in this project.
* The project can be deployed to Heroku using the following steps.

1. Log in to Heroku and create an App
2. At the **Deploy** tab, select **GitHub** as the deployment method.
3. Select your repository name and click **Search**. Once it is found, click **Connect**.
4. Select the branch you want to deploy, then click **Deploy Branch**.
5. The deployment process should happen smoothly if all deployment files are fully functional. Click the button **Open App** at the top of the page to access your App.
6. If the slug size is too large, then add large files not required for the app to the `.slugignore` file.
