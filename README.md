# Mammal Tracking README

---

## Fictional Client Brief

### Client: UK Nature Connect  
*(fictional public engagement and conservation organisation)*

### Background

UK Nature Connect works to increase public engagement with wildlife and nature
across the United Kingdom. The organisation collaborates with educators, local
councils, and conservation groups to make biodiversity data accessible and
meaningful to non-technical audiences.

The client has access to the **National Mammal Atlas Project** dataset, which
contains large volumes of citizen-science mammal observation records. However,
the dataset is currently under-utilised by the general public due to its size
and technical complexity.

---

## Client Objectives

- Increase public interest and engagement with UK mammals  
- Make complex biodiversity data intuitive and interactive  
- Encourage people to explore nature locally and notice wildlife  
- Support long-term conservation awareness through data-driven storytelling  

---

## Client Requirements

The client requests a **public-facing interactive dashboard** that:

- Visualises mammal observation data clearly and engagingly  
- Allows users to explore species, locations, and time trends  
- Goes beyond static visualisation by offering predictive or forward-looking insights  
- Is suitable for non-technical users (e.g. families, schools, community groups)  

---

## My Response / Proposed Solution

### Proposed Approach

To meet the client’s objectives, this project proposes an **AI-enhanced
interactive dashboard** that combines historical data visualisation with a
predictive machine-learning component.

The solution will not only show where mammals have been observed, but will also
estimate the **probability of future mammal sightings by location and time**,
encouraging proactive engagement with nature.

---

## 1. Dashboard Concept

The dashboard will include:

- An interactive map showing historical mammal observations  
- Filters for species, year, and region  
- Time-series charts illustrating trends in mammal reporting  
- Educational annotations explaining patterns and seasonal behaviour  

This supports data storytelling, making complex biodiversity data approachable
for a public audience.

---

## 2. AI Model: Predicting Future Mammal Sightings

### Model Objective

Estimate the probability of mammal presence based on:

- Geographic location (latitude, longitude)  
- Time features (year, month, season)  
- Species or taxonomic group  
- Historical observation density  

### Intended User Experience

- Users select a species (or group) and time window (e.g. “Spring”)  
- The dashboard highlights areas with higher likelihood of sightings  
- Outputs are presented as **probabilities or heatmaps**, not deterministic predictions  

---

## 3. Responsible Use of AI

The AI component is positioned as an **engagement and educational tool**, not a
precise wildlife tracker.

Key considerations:

- Predictions reflect historical reporting patterns, not guaranteed animal presence  
- Outputs are influenced by observer effort and reporting bias  
- Clear disclaimers explain that results are indicative rather than definitive  

This aligns with ethical AI principles and conservation best practices.

---

## 4. Value to the Client

This solution:

- Transforms static biodiversity records into an interactive public experience  
- Encourages local engagement with wildlife  
- Uses AI to promote curiosity rather than passive data consumption  
- Demonstrates responsible and innovative use of data science  

---

## One-Sentence Summary (Assessment-Friendly)

This project transforms UK mammal observation data into an AI-enhanced dashboard
that visualises historical trends and estimates the probability of future mammal
sightings to engage the public with nature.

---

## User Stories and Acceptance Criteria

*(Content unchanged — retained exactly as provided in the project)*

---

## Project Board (Planning & Delivery)

A **Kanban-style project board** was used to plan, track, and document progress
throughout the project lifecycle.

### 🟦 Backlog (Planned)

- Define client brief and project scope 
- Identify analytical questions (spatial, temporal, engagement)  
- Define mammal grouping strategy  
- Identify ethical considerations and data limitations  
- Design dashboard structure and visual components  

---

### 🟨 To Do

- Finalise AI feature set and modelling approach  
- Prepare training and test datasets 
- Draft public-facing explanations of AI behaviour  
- Prepare Streamlit layout and navigation  
- Finalise README and documentation  

---

### 🟧 In Progress

- Exploratory data analysis (EDA)  
- Temporal coverage assessment and cleaning  
- Mammal grouping and taxonomy mapping  
- Spatial density visualisation  
- Statistical foundations documentation  
- Interactive mapping and performance optimisation  

---

### 🟩 Done

- Environment setup and dependency management  
- Data loading and validation  
- Missing data analysis and documentation  
- Removal of unusable fields (e.g. fully missing columns)  
- Identification and treatment of unreliable early-year data  
- Justification of cleaning decisions  
- Creation of interactive visualisations  
- User stories and acceptance criteria written  
- Client brief and solution definition completed  

---

### 🟥 Risks & Limitations (Monitored)

- Reporting bias and uneven observation effort  
- Record density does not represent true population size  
- Ethical considerations around wildlife location data  
- Performance constraints with large datasets  
- Risk of misinterpreting AI outputs as deterministic predictions  

---

## Deployment Reminders

- Set the `.python-version` to a **Heroku-22 supported runtime** closest to the
  development environment  
- Deploy via Heroku using GitHub integration  

### Deployment Steps

1. Log in to Heroku and create an app  
2. In the **Deploy** tab, select **GitHub**  
3. Connect the repository and select the deployment branch  
4. Click **Deploy Branch**  
5. Open the deployed app once the build completes  
6. If slug size is too large, exclude non-essential files using `.slugignore`  
