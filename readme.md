
## IHT/FYP Repository


**Thesis Title:**
> Optimal Bidding Overtime Strategy for Online Art Auctions: Evidence from Chinese Art Auction Houses

**Author:**
> Tang Hanyang

**About:**
> The integrated graduation thesis & project under National University of Singapore:
>
>  Department of Economics, Faculty of Arts & Social Sciences: 
>  - Integrated Honours Thesis (IHT)
>  - For Bachelor of Social Sciences (Honours) in Economics
>  - Supervisor: Prof. Lu Jingfeng
>
> 
>  Department of Information Systems and Analytics, School of Computing
>  - Final Year Project (FYP)
>  - For Bachelor of Sciences (Honours) in Business Analytics
>  - Supervisor: A/P Zhai Yingda
>
> 
> Timeframe: January 2023 - November 2023

**Abstract:**
>The paper studies the impact of bidding overtime in online art auctions. We identify two contrasting overtime bidding 
  mechanisms influencing the final winning price: the positive effect of valuation learning and the negative effect of 
  attention cost. We define a theoretical auction model with bidding mechanisms that yield an optimum outcome through 
  Monte Carlo simulation. By evaluating four bidding overtime durations at six Chinese art auction houses, we 
  consistently observe a positive effect on final prices with longer overtime policies in all settings, from which we 
  validate the bidding mechanisms and propose an optimal design of overtime duration at 3 minutes. The paper then 
  discusses whether these effects apply to lower-value eBay auctions and physical auctions.


## Contents of the Repository

### Deliverables
-  Final Report [Public]

    >  📕 report / [final_report_public.pdf](report/final_report_public.pdf)
    >
    > This is the public release of the final report on the analysis of bidding overtime and the optimal policies 
    theoretically and empirically.


### Online Art Auction Dataset on Overtime
- Full Dataset [Public]
  >  📊 public_data / [1_public_full_dataset.xlsx](public_data/1_public_full_dataset.xlsx)
  >
  > This dataset is the processed raw data in wide form and has been anonymized. It contains all the data we collected
  > from the six traditional Chinese art auction houses.

- Processed Full Dataset [Public]
  >  📊 public_data / [2_processed_full_dataset.xlsx](public_data/2_processed_full_dataset.xlsx)
  >
  > This dataset is processed from the public full dataset and calculates all inferred parameters.

- Processed Sampled Dataset [Public]
  >  📊 public_data / [3_processed_sample_dataset.xlsx](public_data/3_processed_sample_dataset.xlsx)
  >
  > This dataset balances items under each specific overtime policy (Short, Intermediate, Long) via a random draw
  > from the 3-minute overtime items (over-abundant) cut to half. This dataset includes expert scores and expert recommended items.
  > It is the dataset used for reduced form analysis.

- Raw Data Records from Each Auction [Confidential]
  >  🔒 data / special / *
  > 
  >  🔒 data / standard / *
  > 
  >  🔒 data / data_list.xlsx
  > 
  > Due to confidentiality, raw and non-anonymized data records under the data folder are not included in the code package. Available upon request only.

### Python Codes
- Auction Data Processor
  > 💾 [process_data.py](process_data.py)
  >
  > The auction data processor is the data processing pipeline that reads in raw data formats from auction houses
  > and transforms data into desirable formats for analysis and visualisation. Note: It requires the raw dataset to
  > process. The current public datasets are generated through the pipeline.

- Auction Data Analyzer
  > 💾 [analyze_data.py](analyze_data.py)
  > 
  > The auction data analyzer completes multiple complex calculations and data visualisations, including calculation
  > of the bids interval, drawing the price growth path and CDF of bidding intervals.
  >
  > Several price growth path charts are provided as examples under the output / charts folder.

- Structural Auction Model Simulator
  > 💾 [game_simulation.py](game_simulation.py)
  >
  > The Monte Carlo simulator for the proposed auction model with bidding mechanisms in Section 3. Functions are
  > annotated inside the file on how to tune and simulate the model.

- Supporting Functions

### STATA Codes
- Linear Regression
  >  📑 stata / [section_5_regression.do](stata/section_5_regression.do)
  >
  > The STATA do file performs reduced form regressions across multiple model classifications under Section 5.

## Last Update

- November 8, 2023
