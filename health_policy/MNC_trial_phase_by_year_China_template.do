clear all
set more off
use "/Users/wangmengting/Desktop/global_trial.dta", clear

gen astrazeneca_flag = regexm(lower(申办者), "pfizer")
gen china_flag = regexm(lower(国家地区), "china")
keep if pfizer_flag & china_flag

gen 分期标准 = lower(strtrim(试验分期))

drop if inlist(分期标准, "n/a", "not applicable", "")

gen 分期归一 = .
replace 分期归一 = 1 if 分期标准 == "phase 1"
replace 分期归一 = 2 if inlist(分期标准, "phase 1/phase 2", "phase 2")
replace 分期归一 = 3 if inlist(分期标准, "phase 2/phase 3", "phase 3")
replace 分期归一 = 4 if 分期标准 == "phase 4"

label define phase_lbl 1 "Phase 1" 2 "Phase 2" 3 "Phase 3" 4 "Phase 4"
label values 分期归一 phase_lbl

drop if missing(分期归一)

gen 开始日期_数 = date(开始日期, "YMD")
format 开始日期_数 %td
gen 开始年份 = year(开始日期_数)

gen one = 1

collapse (sum) 试验数 = one, by(开始年份 分期归一)

reshape wide 试验数, i(开始年份) j(分期归一)

rename 试验数1 Phase_1
rename 试验数2 Phase_2
rename 试验数3 Phase_3
rename 试验数4 Phase_4

export excel using pfizer_china_trial_counts_cleaned_final.xlsx, firstrow(variables) replace
