* IHT/FYP Codes Submission

* STATA code for reduced form regressions on Section 5:

* condition: the working directory is usder the "stata" directory.

* use full dataset for overtime item regressions
clear
import excel "../public_data/2_processed_full_dataset.xlsx", sheet("Full_Dataset") firstrow

* regression on final price ~ overtime items
reg winning_bid is_overtime_item, r

* use sampled dataset for overtime policy analysis
clear
import excel "../public_data/3_processed_sample_dataset.xlsx", sheet("Sampled_Dataset") firstrow

* regression on final price ~ overtime length
reg winning_bid overtime_length, r

* regression on final price ~ overtime bids
reg winning_bid overtime_bids, r

* check non-overtime data removed
generate subset = (is_overtime_item == 1)
keep if subset==1

* overtime duration dummy variables
gen overtime_60 = overtime_rule==60 if !missing(overtime_rule)
gen overtime_120 = overtime_rule==120 if !missing(overtime_rule)
gen overtime_180 = overtime_rule==180 if !missing(overtime_rule)
gen overtime_300 = overtime_rule==300 if !missing(overtime_rule)

* overtime duration groups
gen overtime_less_180 = overtime_rule <= 120 if !missing(overtime_rule)
gen overtime_over_180 = overtime_rule > 120 if !missing(overtime_rule)

* regression for Final Price ~ Item Value + Overtime Effect + Confounding Factors

* setup 1 - size moderated
reg winning_bid overtime_120 overtime_180 overtime_300, r
reg winning_bid overtime_180 overtime_300, r
reg winning_bid overtime_over_180, r

* setup 2-5 - expert score method
reg winning_bid overtime_120 overtime_180 overtime_300 expert_1_score, r
reg winning_bid overtime_180 overtime_300 expert_1_score, r
reg winning_bid overtime_over_180 expert_1_score, r

reg winning_bid overtime_120 overtime_180 overtime_300 expert_2_score, r
reg winning_bid overtime_180 overtime_300 expert_2_score, r
reg winning_bid overtime_over_180 expert_2_score, r

reg winning_bid overtime_120 overtime_180 overtime_300 expert_3_score, r
reg winning_bid overtime_180 overtime_300 expert_3_score, r
reg winning_bid overtime_over_180 expert_3_score, r

reg winning_bid overtime_120 overtime_180 overtime_300 expert_4_score, r
reg winning_bid overtime_180 overtime_300 expert_4_score, r
reg winning_bid overtime_over_180 expert_4_score, r

* setup 6 - normal bid intensity method
reg winning_bid overtime_120 overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_over_180 normal_bid_intensity, r

* following regressions use avg expert scores

* baseline comparison by avg expert scores
reg winning_bid overtime_120 overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_over_180 expert_valuation_score, r

reg winning_bid overtime_120 overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_over_180 normal_bid_intensity, r

* subgroup - price >= cny 5000
keep if final_price_over_5000==1

reg winning_bid overtime_120 overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_over_180 expert_valuation_score, r

reg winning_bid overtime_120 overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_over_180 normal_bid_intensity, r

* subgroup - price >= cny 10000
keep if final_price_over_10000==1

reg winning_bid overtime_120 overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_over_180 expert_valuation_score, r

reg winning_bid overtime_120 overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_over_180 normal_bid_intensity, r

* subgroup - price >= cny 20000
keep if final_price_over_20000==1

reg winning_bid overtime_120 overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_over_180 expert_valuation_score, r

reg winning_bid overtime_120 overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_over_180 normal_bid_intensity, r

* reload sampled dataset
clear
import excel "3_processed_sample_dataset.xlsx", sheet("Sampled_Dataset") firstrow
gen overtime_60 = overtime_rule==60 if !missing(overtime_rule)
gen overtime_120 = overtime_rule==120 if !missing(overtime_rule)
gen overtime_180 = overtime_rule==180 if !missing(overtime_rule)
gen overtime_300 = overtime_rule==300 if !missing(overtime_rule)
gen overtime_less_180 = overtime_rule <= 120 if !missing(overtime_rule)
gen overtime_over_180 = overtime_rule > 120 if !missing(overtime_rule)

* subgroup - expert selected items with by least one expert
keep if expert_selection_score >= 1

reg winning_bid overtime_120 overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_over_180 expert_valuation_score, r

reg winning_bid overtime_120 overtime_180 overtime_300 expert_selection_score normal_bid_intensity, r
reg winning_bid overtime_180 overtime_300 expert_selection_score normal_bid_intensity, r
reg winning_bid overtime_over_180 expert_selection_score normal_bid_intensity, r

* reload sampled dataset
clear
import excel "3_processed_sample_dataset.xlsx", sheet("Sampled_Dataset") firstrow
gen overtime_60 = overtime_rule==60 if !missing(overtime_rule)
gen overtime_120 = overtime_rule==120 if !missing(overtime_rule)
gen overtime_180 = overtime_rule==180 if !missing(overtime_rule)
gen overtime_300 = overtime_rule==300 if !missing(overtime_rule)
gen overtime_less_180 = overtime_rule <= 120 if !missing(overtime_rule)
gen overtime_over_180 = overtime_rule > 120 if !missing(overtime_rule)

* subgroup - item type = calligraphy
keep if item_type=="calligraphy"

reg winning_bid overtime_120 overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_180 overtime_300 expert_valuation_score, r
reg winning_bid overtime_over_180 expert_valuation_score, r

reg winning_bid overtime_120 overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_180 overtime_300 normal_bid_intensity, r
reg winning_bid overtime_over_180 normal_bid_intensity, r
