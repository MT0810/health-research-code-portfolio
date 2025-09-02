clear all
set more off
use "/Users/wangmengting/Desktop/global_trial.dta", clear

gen AstraZeneca_flag = regexm(lower(申办者), "pfizer")
gen china_flag = regexm(lower(国家地区), "china")
keep if pfizer_flag & china_flag
count

gen 开始日期_数 = date(开始日期, "YMD")
format 开始日期_数 %td
gen 开始年份 = year(开始日期_数)

gen one = 1
collapse (sum) 试验数 = one, by(开始年份 试验状态)

gen 状态变量名 = lower(itrim(试验状态))
replace 状态变量名 = subinstr(状态变量名, ",", "", .)
replace 状态变量名 = subinstr(状态变量名, " ", "_", .)

collapse (sum) 试验数, by(开始年份 状态变量名)

reshape wide 试验数, i(开始年份) j(状态变量名) string

export excel using pfizer_trial_status_by_year.xlsx, firstrow(variables) replace
