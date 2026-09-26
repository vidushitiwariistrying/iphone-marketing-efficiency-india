Research Question: Did the iPhone 18 series launch in India yield higher marketing efficiency compared to the iPhone 17 series?  

Hypothesis: YoY marketing conversion rate experienced an increase due to higher localised demand after the product announcement.

Falsification Criteria: The hypothesis fails if (a) The efficiency ratio drops in the second year, or (b) The 7-Day decline is identical in both cases.

The Setup (7-Day window): Bounded to the first 7 days since the keynote event which cover the product announcement and Pre-ordering window both. Expanding beyond first 7 days was avoided to eliminate noise as PR buzz approaches 0 on these days.

Data Cleaning: Built a python pipeline to handle Google Trends CSV files and resolved excel formatting issues, auto-header offsets etc without using Dropna() in order to keep the row alignment intact.

Formula used:  Marketing Efficiency ratio= (Sum of Consumer Search Interest)/(Sum of PR Buzz Score)

Quantitative Results: 

iPhone 17 series efficiency- 2.39
iPhone 18 series efficiency- 2.49

Conclusion:

(a) iPhone 18 series had a higher marketing efficiency with approximately a 4.2% gap.

(b) The total search demand was identical in both cases (306 points). However, Apple required less PR buzz (123 vs 128) to generate the same total demand during the 18 series launch.

(c) Hypothesis was supported and the falsification criteria wasn't triggered.


