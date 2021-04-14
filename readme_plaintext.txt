cs5010-project
CS 5010 Semester Project - by Global Warning! 

Nima Beheshti, Jess Cheu, Ben Feciura, Gary Mitchell

---

Overview:

Because greenhouse gas emissions, particularly in the form of CO2, are the
primary factor influencing global warming, for our investigation we examined
historical data dealing with quantities of CO2 emitted by each country from
1751 to 2017.

We hoped to learn about some of the major events that influence emissions as
well as to get a better perspective on the current state of the emissions
issue.

We gained a better context for the issue of emissions as a whole and gained valuable experience in carrying out the data science process including validation, testing, user experience design, and visualization.

---

Descriptions of Files:

>
> cs_proj_analysis.py
>
Includes the data cleaning and analysis we performed
as part of our own investigations, and from which the information discussed
in our results section originated.

Requires cs_proj_functions.py to run. Visualization results can be found in
/Visualization_Output/.
>
> cs_proj_viz_tool.py
>
The user-oriented visualization tool we designed
to allow users to subset the data as they choose. With the subsetted data,
they can produce their own visualizations and learn a bit more about the
context for the data.

Requires cs_proj_functions.py to run, and is designed to use the cleaned
version of the dataset, data_cleaned.csv, or any subset of this dataset.
>
> cs_proj_functions.py
>
Contains functions we built to use throughout the
project.
>
> cs_proj_functions_test.py
>
Contains unit tests used to validate cs_proj_functions.py.
>
>co2_emission.csv
>
The raw dataset for our project.
>
>data_cleaned.csv
>
The result of data cleaning that was used in the majority of our analyses.

---

Subsets of Data:

In /Subsets/ we have placed many of the data subsets that resulted from our investigations.

---

Report and Presentation:

In /Presentation/, we have included copies of our written report (Report.pdf) and our long- and short-form visuals (Slides.pdf and Slides_LIVE.pdf) for the video presentation.

---

Sources:

Original Data: https://www.kaggle.com/yoannboyere/co2-ghg-emissionsdata 

Historic CO2 Concentration Levels: www.climate.gov/news-features/understanding-climate/climate-change-atmospheric-carbon-dioxide

Safe Concentration of Atmospheric CO2: www.dhs.wisconsin.gov/chemical/carbondioxide.htm "Wisconsin Department of Health Services"

Carbon Contribution of Single-Use Plastics: https://www.omnicalculator.com/ecology/plastic-footprint

Carbon Contribution of Commuting by Internal-Combustion Vehicles: itstillruns.com/far-americans-drive-work-average-7446397.html

Carbon Contribution of Daily Activities: https://www.clackamas.us/sustainability/tips.html
