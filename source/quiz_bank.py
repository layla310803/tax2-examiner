# Quick-quiz question bank: short type-in questions on knowledge and application.
# These are NOT taken from the past papers. Figures are for the 2025/2026 years of assessment
# (the ones the 2025 and 2026 papers use). Review when rates or thresholds change.
#
# Each entry is (question, model answer, check):
#   check = a number          -> the typed answer is marked right if it is that number
#   check = a regex (string)  -> marked right if the typed answer matches it (case-insensitive)
#   check = [regex, regex]    -> marked right only if every regex matches
# The student can always override the automatic mark after seeing the model answer.

NO = r"\bno\b|\bnot\b|cannot|can't|\bnil\b|\bnone\b"
YES = r"\byes\b"

BANK = {

# ------------------------------------------------------------------ Individuals
"ind": [
 ("What is the primary rebate for a natural person (in rand)?", "R17 235 (s6).", 17235),
 ("What additional (secondary) rebate does a person aged 65 or older get, on top of the primary rebate?", "R9 444 (s6). A further R3 145 applies from age 75.", 9444),
 ("How much local interest is exempt each year for a natural person under 65?", "R23 800 (s10(1)(i)). It is R34 500 from age 65.", 23800),
 ("Thabo (40) earns R30 000 interest from a South African bank. How much of it is taxable?", "R6 200: R30 000 less the R23 800 exemption in s10(1)(i).", 6200),
 ("Nomsa is 68 and earns R30 000 local interest. How much of it is taxable?", "Nil. The exemption from age 65 is R34 500, which covers all of it.", 0),
 ("The s11F deduction for retirement fund contributions is capped at what rand amount per year?", "R350 000.", 350000),
 ("Apart from the rand cap, the s11F deduction is limited to what percentage of the higher of remuneration or taxable income?", "27.5%.", 27.5),
 ("Lerato has remuneration of R800 000 and taxable income (before s11F, no capital gains) of R900 000. She contributed R260 000 to her pension fund. What is her s11F deduction?",
  "R247 500: 27.5% x R900 000 (the higher amount), which is below both her contributions and the R350 000 cap. The other R12 500 carries forward.", 247500),
 ("What happens to retirement fund contributions that exceed the s11F limit for the year?", "They are carried forward and treated as contributions made in the following year.", r"carr|roll|next year|following year"),
 ("The s18A deduction for donations to a PBO is limited to what percentage of taxable income?", "10% of taxable income before the s18A deduction. Any excess carries forward.", 10),
 ("Which deduction is calculated last when working out an individual's taxable income: s11F or s18A?", "s18A. The order is: include the taxable capital gain, then s11F, then s18A.", r"18\s*a|donation"),
 ("A taxpayer, their spouse and two children belong to a medical scheme for the full year. What is the annual s6A medical scheme fees tax credit?",
  "R14 640: (R364 + R364 + R246 + R246) x 12.", 14640),
 ("For a person under 65 with no disability, the s6B credit is 25% of the amount by which their medical costs exceed what percentage of taxable income?",
  "7.5% of taxable income. The medical costs are the scheme contributions above four times the s6A credit plus qualifying out-of-pocket expenses, taken together.", 7.5),
 ("How is a dividend from a South African company treated for normal tax in the hands of an individual?", "It is exempt from normal tax (s10(1)(k)(i)). Dividends tax of 20% is withheld instead.", r"exempt"),
 ("Maintenance received from a former spouse under a divorce order: taxable or exempt?", "Exempt (s10(1)(u)).", r"exempt"),
 ("What is the maximum marginal rate of normal tax for a natural person (percent)?", "45%, on taxable income above R1 817 000.", 45),
 ("An individual's only capital gain for the year is R140 000. What taxable capital gain is included in taxable income?", "R40 000: (R140 000 less the R40 000 annual exclusion) x 40%.", 40000),
],

# ------------------------------------------------------------------ Employees' tax
"emp": [
 ("Employees' tax withheld during a month must be paid to SARS within how many days after the end of that month?", "7 days (para 2(1) of the Fourth Schedule).", 7),
 ("What percentage of a travel allowance is normally included in remuneration for employees' tax?", "80%.", 80),
 ("If the employer is satisfied that at least 80% of the vehicle's use will be for business, what percentage of the travel allowance is included in remuneration?", "20%.", 20),
 ("An employee receives a travel allowance of R6 000 a month with no evidence of high business use. How much is included in monthly remuneration?", "R4 800 (80% x R6 000).", 4800),
 ("What percentage of the company-car fringe benefit is normally included in remuneration for employees' tax?", "80% (20% if the employer is satisfied that at least 80% of use is for business).", 80),
 ("Under s7B, when is variable remuneration such as a bonus, commission or overtime taxed in the employee's hands?", "When it is paid to the employee, not when it accrues. The employer also only deducts it when paid.", r"paid|payment|pays"),
 ("A bonus is awarded in February 2025 but only paid in March 2025. In which year of assessment (e.g. 2025 or 2026) is the employee taxed on it?", "2026. Under s7B it is taxed when paid, and March 2025 falls in the 2026 year of assessment.", 2026),
 ("An employee earns a salary of R40 000 a month and contributes R3 000 a month to the employer's pension fund. On what balance of remuneration is employees' tax calculated?",
  "R37 000. The pension contribution is deducted under para 2(4) of the Fourth Schedule.", 37000),
 ("A subsistence allowance is paid in advance but the employee never spends a night away and does not repay it. By when does it become remuneration?",
  "At the end of the month following the month in which it was paid (s8(1)(a)(ii)).", r"following month|month following|next month|month after|subsequent month"),
 ("A person paid at regular intervals and subject to the client's control is still treated as an independent contractor if they employ at least how many full-time unconnected employees throughout the year?", "Three.", 3),
 ("At what rate must employees' tax be withheld from fees paid to a personal service provider that is a company (percent)?", "27%. For a trust it is 45%.", 27),
 ("One test for a personal service provider is that more than what percentage of its income from services comes from one client?", "80%.", 80),
 ("A labour broker does not hold an exemption certificate. What must the client do when paying the broker?", "Withhold employees' tax from the payment.", r"withh|deduct|paye|employees.? tax"),
 ("Does an employer take the s6A medical scheme fees tax credit into account when calculating monthly employees' tax?", "Yes (para 9(6) of the Fourth Schedule).", YES),
 ("Donations made through the payroll may be taken into account for employees' tax up to what percentage of remuneration?", "5% of remuneration after the other para 2(4) deductions.", 5),
 ("If an employer fails to withhold employees' tax, who is personally liable to SARS for it?", "The employer (para 5 of the Fourth Schedule), with a right to recover it from the employee.", r"employer"),
],

# ------------------------------------------------------------------ Assessed losses
"loss": [
 ("A company's set-off of an assessed loss brought forward is limited to the higher of R1 million or what percentage of taxable income before the set-off?", "80% (s20).", 80),
 ("A company has taxable income of R5 000 000 before setting off an assessed loss brought forward of R6 000 000. What is its taxable income for the year?",
  "R1 000 000. The set-off is limited to the higher of R1 million or 80% x R5 000 000 = R4 000 000. The other R2 000 000 is carried forward.", 1000000),
 ("A company has taxable income of R800 000 before setting off an assessed loss brought forward of R3 000 000. How much assessed loss is carried forward to next year?",
  "R2 200 000. The limit is the higher of R1 million or R640 000, so the full R800 000 is sheltered and taxable income is nil.", 2200000),
 ("Does the 80% limitation on setting off assessed losses apply to natural persons?", "No. It applies only to companies.", NO + r"|only compan"),
 ("What must a company do during a year to keep its right to carry forward its assessed loss?", "Carry on a trade during that year. If it does not trade, the balance of the assessed loss is forfeited.", r"trad"),
 ("Section 20A ring-fencing can only apply to a natural person whose taxable income reaches what level?", "The level at which the maximum marginal rate (45%) applies, R1 817 000 for the 2025 and 2026 years, measured before setting off the losses. A lower trigger has been proposed for years starting on or after 1 March 2026, so check the current Act for later years.", r"max|highest|top|45|1\s?817"),
 ("Under the 'three-out-of-five-years' rule in s20A, a trade is caught if it made losses in at least how many of the last five years (including the current year)?", "Three.", 3),
 ("Renting out residential accommodation is a suspect trade unless at least what percentage of it is used by people who are not relatives for at least half the year?", "80%.", 80),
 ("A trade falls within s20A. On what basis can the taxpayer still escape ring-fencing?", "The facts and circumstances test: a reasonable prospect of deriving taxable income from the trade within a reasonable period (s20A(3)).", r"prospect|reasonable period|facts and circumstances"),
 ("For a suspect trade (other than farming), the escape in s20A(3) is not available once losses have arisen in at least how many of the last ten years?", "Six.", 6),
 ("Against what income can a ring-fenced assessed loss be set off in later years?", "Only against income from that same trade.", r"same trade|that trade|same activity|that activity"),
 ("Can an assessed loss from a trade carried on outside South Africa be set off against South African income?", "No (proviso to s20(1)). It is carried forward against future foreign trade income.", NO),
],

# ------------------------------------------------------------------ Estate duty
"ed": [
 ("At what rate is estate duty charged on the first R30 million of the dutiable amount (percent)?", "20%. Above R30 million the rate is 25%.", 20),
 ("What is the s4A abatement (in rand)?", "R3 500 000.", 3500000),
 ("A husband died first and his estate used R1 575 000 of the abatement. What abatement is available to his widow's estate when she later dies?",
  "R5 425 000: R7 000 000 less the R1 575 000 used by the first-dying spouse's estate.", 5425000),
 ("A deceased leaves a house worth R2 million to his surviving spouse. What is the estate duty treatment?", "It is included as property and then deducted under s4(q), so it adds nothing to the net estate.", r"deduct|4\s*\(?q"),
 ("Proceeds of a South African life policy on the deceased's life are paid directly to his daughter. Property, deemed property, or excluded?", "Deemed property (s3(3)(a)), less any premiums plus 6% interest that the daughter herself paid.", r"deemed"),
 ("Is a lump sum paid by a pension fund on the member's death included in the estate?", "No. Retirement fund benefits are excluded from property.", NO + r"|exclu"),
 ("The executor's remuneration is set by tariff at what percentage of the gross value of the assets?", "3.5%. It is deductible as an administration cost.", 3.5),
 ("A South African resident dies owning a flat in London that she bought while resident here. Is it included in her estate?", "Yes. A resident's worldwide property is included.", YES + r"|includ"),
 ("A deceased who was not ordinarily resident in South Africa owned a flat in London. Is it included in the estate for South African estate duty?", "No. Only a non-resident's South African property is included.", NO + r"|exclu"),
 ("Who is liable for the estate duty attributable to life policy proceeds paid directly to a beneficiary?", "The beneficiary who receives the proceeds (s11).", r"beneficiar|recipient|person (who|that) receive"),
 ("Is the deceased's final income tax liability, including CGT triggered by death, deductible in calculating the net estate?", "Yes, as a debt due at death (s4(b)).", YES + r"|deduct"),
 ("The net value of an estate is R6 000 000 and no abatement was used by a predeceased spouse. What is the estate duty?", "R500 000: (R6 000 000 less R3 500 000) x 20%.", 500000),
 ("An estate has property of R9 000 000, debts and administration costs of R500 000, and a R3 000 000 bequest to the surviving spouse. What is the estate duty?",
  "R400 000. Net estate R5 500 000, less the R3 500 000 abatement gives a dutiable amount of R2 000 000, at 20%.", 400000),
 ("At what annual rate is a usufruct capitalised when valuing it for estate duty (percent)?", "12% a year over the life expectancy of the person entitled to it.", 12),
 ("A deceased leaves R500 000 to a registered public benefit organisation. What is the estate duty treatment?", "It is deductible from the estate (s4(h)).", r"deduct"),
],

# ------------------------------------------------------------------ VAT
"vat": [
 ("What is the standard rate of VAT (percent)?", "15%.", 15),
 ("A vendor sells goods for R230 000 including VAT. How much output tax is included?", "R30 000 (R230 000 x 15/115).", 30000),
 ("Registration is compulsory once taxable supplies exceed what amount in a 12-month period?", "R1 million.", 1000000),
 ("A person may register voluntarily once taxable supplies have exceeded what amount in the past 12 months?", "R50 000.", 50000),
 ("A manufacturer buys a sedan for its sales manager to use. Can it claim input tax on the purchase?", "No. Input tax on a motor car is denied (s17(2)(c)) unless the vendor is, for example, a car dealer or car rental business.", NO + r"|denied"),
 ("A vendor takes clients to lunch. Can it claim input tax on the restaurant bill?", "No. Input tax on entertainment is denied (s17(2)(a)).", NO + r"|denied"),
 ("Letting a flat as a dwelling: is this standard-rated, zero-rated or exempt?", "Exempt.", r"exempt"),
 ("At what rate is a direct export of goods taxed?", "Zero-rated (0%).", r"zero|\b0\s*%|\b0\b"),
 ("Can a vendor claim input tax on expenses incurred to make exempt supplies?", "No. Input tax is only claimable to the extent the expense is for making taxable supplies.", NO),
 ("Can a vendor claim input tax on expenses incurred to make zero-rated supplies?", "Yes. Zero-rated supplies are taxable supplies.", YES),
 ("Under the general rule, when does the time of supply occur?", "At the earlier of the time an invoice is issued or any payment is received (s9(1)).", [r"invoice", r"pay|receiv"]),
 ("A vendor supplies goods for no consideration to a connected person who cannot claim the full input tax. What is the value of the supply?", "The open market value (s10(4)).", r"open market|omv|market value"),
 ("A vendor buys a second-hand machine from a non-vendor for R115 000 cash (its open market value is R120 000) to use wholly for taxable supplies. What notional input tax can it claim?",
  "R15 000: 15/115 x R115 000, the lesser of the consideration and the open market value.", 15000),
 ("For the deemed supply when an employee has the use of a motor car on which input tax was denied, what percentage of the determined value is the monthly consideration?", "0.3% a month (0.6% where input tax was not denied).", 0.3),
 ("A vendor takes trading stock out of the business for private use. On what value is output tax calculated?", "The open market value of the goods (s18(1) change in use).", r"open market|omv|market value"),
 ("A vendor's insurer pays out R650 000 for a delivery truck that was written off. How much output tax must the vendor account for?", "R84 783 (R650 000 x 15/115), a deemed supply under s8(8).", 84783),
 ("A vendor on the invoice basis writes off a bad debt of R23 000 (including VAT). How much input tax can it claim?", "R3 000 (R23 000 x 15/115), under s22(1).", 3000),
 ("A vendor that claimed input tax must account for output tax on a creditor it has still not paid after how many months?", "12 months (s22(3)).", 12),
 ("A full tax invoice is required once the consideration for a supply exceeds what amount?", "R5 000. An abridged tax invoice is enough up to that amount.", 5000),
 ("A vendor must file monthly (Category C) once its taxable supplies exceed what amount in a 12-month period?", "R30 million.", 30000000),
 ("A business is sold as a going concern and all the requirements are met. At what rate is the sale taxed?", "Zero-rated (0%).", r"zero|\b0\s*%|\b0\b"),
],

# ------------------------------------------------------------------ Capital allowances
"cap": [
 ("What percentage of cost is allowed in the first year on new and unused manufacturing plant under s12C?", "40%, then 20% in each of the next three years.", 40),
 ("What annual percentage is allowed under s12C on second-hand manufacturing plant?", "20% a year for five years.", 20),
 ("A small business corporation brings new manufacturing plant into use. What percentage of cost can it deduct in that year?", "100% (s12E(1)).", 100),
 ("A small business corporation buys a non-manufacturing asset for R600 000 and uses the s12E(1A) allowance. What is the allowance in the second year?", "R180 000 (30%). The pattern is 50%, 30%, 20%.", 180000),
 ("Is the s12C allowance apportioned when the asset is used for only part of the year?", "No. The full percentage is allowed in the year the asset is brought into use.", NO),
 ("A machine costing R120 000 with a four-year write-off period under s11(e) is brought into use on 1 October. The year ends on 31 December. What is the wear-and-tear allowance for that year?",
  "R7 500: R120 000 / 4 x 3/12. Section 11(e) is apportioned for the period of use.", 7500),
 ("What annual percentage is allowed on a building used in a process of manufacture under s13(1)?", "5%.", 5),
 ("A company buys a second-hand office block. Can it claim the s13quin allowance?", "No. Section 13quin requires a new and unused building (or new and unused improvements).", NO),
 ("To claim the s13sex allowance on residential units, the taxpayer must own at least how many new and unused units in South Africa?", "Five.", 5),
 ("A machine cost R500 000 and R300 000 of allowances have been claimed. It is sold for R550 000. What is the s8(4)(a) recoupment?",
  "R300 000. Proceeds are limited to cost (R500 000) less the tax value of R200 000. The R50 000 above cost is dealt with under CGT.", 300000),
 ("A machine cost R400 000 and R250 000 of allowances have been claimed. It is sold to an unconnected buyer for R100 000. What s11(o) allowance can be claimed?",
  "R50 000: tax value of R150 000 less proceeds of R100 000.", 50000),
 ("To defer a recoupment on a destroyed asset under s8(4)(e), the contract for the replacement must be concluded within how many months of the disposal?", "12 months. The replacement must be brought into use within three years.", 12),
 ("What percentage of cost is allowed in the first year on farming machinery under s12B?", "50%, then 30% and 20%.", 50),
 ("A VAT vendor buys new manufacturing plant for R230 000 including VAT and claims the input tax. What is the first-year s12C allowance?", "R80 000: 40% x R200 000. The cost excludes VAT that was claimed as input tax.", 80000),
 ("A vendor buys a motor car on which input tax is denied. Does the cost for wear and tear include the VAT?", "Yes. VAT that cannot be claimed forms part of the cost.", YES + r"|includ"),
 ("A company donates a machine on which allowances were claimed. For the recoupment, what amount is it deemed to have received?", "The market value of the machine (s8(4)(k)).", r"market value"),
],

# ------------------------------------------------------------------ Leases
"lease": [
 ("A lessee deducts a lease premium over the period of the lease, but that period is capped at how many years?", "25 years (s11(f)).", 25),
 ("A lessee pays a lease premium of R240 000 for a 10-year lease starting on 1 July. Its year ends on 31 December. What is the s11(f) deduction in the first year?",
  "R12 000: R240 000 / 120 months x 6 months.", 12000),
 ("How is a lease premium taxed in the lessor's hands?", "It is included in gross income in full in the year it is received or accrues (para (g) of the gross income definition).", r"full|para(graph)?\s*\(?g\b|gross income"),
 ("Can the lessee deduct a lease premium under s11(f) if the premium is not income in the lessor's hands (for example, the lessor is exempt from tax)?", "No.", NO),
 ("A 10-year lease starts on 1 January 2025 and obliges the lessee to make improvements of R360 000. They are completed on 1 January 2026. What is the s11(g) deduction for the year ending 31 December 2026?",
  "R40 000: R360 000 over the nine years of the lease remaining from completion.", 40000),
 ("A lease obliges the lessee to spend R500 000 on improvements. The lessee spends R650 000. On what amount is the s11(g) allowance based?", "R500 000, the amount stipulated in the lease.", 500000),
 ("A lease obliges the lessee to make improvements but states no amount. On what value is the s11(g) allowance based?", "The fair and reasonable value of the improvements.", r"fair|reasonable"),
 ("How are obligatory leasehold improvements taxed in the lessor's hands?", "The stipulated amount (or the fair and reasonable value) is included in gross income under para (h) when the right to have the improvements made accrues.", r"para(graph)?\s*\(?h\b|gross income|includ"),
 ("The lessor's relief allowance in s11(h) is denied where the lessor or lessee is a company and the other party holds more than what percentage of any class of its shares?",
  "50%. It is also denied where a third person holds more than 50% of the shares in both companies.", 50),
 ("A lessee is obliged to improve a building leased from a provincial government, so s11(g) is not available. Which section deems the lessee to own the improvement so that capital allowances can be claimed?", "Section 12N.", r"12\s*n"),
 ("A lease is terminated before the lessee has deducted the full s11(g) allowance. What happens to the balance?", "The balance not yet allowed is deducted in the year the lease is terminated. (For an unclaimed lease premium under s11(f) the opposite applies: no further deduction.)", r"^(?!.*(not deduct|not allow|not claim|\blost\b|forfeit)).*(deduct|allowed|claim)"),
],

# ------------------------------------------------------------------ Fringe benefits
"fringe": [
 ("For a company car, what percentage of the determined value is the fringe benefit each month?", "3.5% (3.25% if the car was bought with a maintenance plan).", 3.5),
 ("What is the monthly percentage for a company car that was bought together with a maintenance plan?", "3.25%.", 3.25),
 ("The official rate of interest for a rand loan is the repo rate plus how many percentage points?", "One percentage point (100 basis points).", 1),
 ("An employer pays an employee's medical scheme contributions. Is this a taxable benefit?", "Yes, for the full amount (para 12A). The employee is treated as having paid it for the s6A credit.", YES + r"|taxable|fringe"),
 ("An employer contributes to a pension fund for an employee. Is the contribution a taxable benefit?", "Yes (para 12D). The employee is treated as having made the contribution for s11F.", YES + r"|taxable|fringe"),
 ("A long-service award in the form of an asset is not taxed up to what value?", "R5 000.", 5000),
 ("In the residential accommodation formula (A - B) x C/100 x D/12, what is the abatement B?", "R95 750.", 95750),
 ("The benefit from the private use of an employer's asset (not accommodation or a vehicle) is what annual percentage of the lesser of its cost or market value?", "15% a year.", 15),
],

# ------------------------------------------------------------------ Companies
"co": [
 ("What is the normal tax rate for a company (percent)?", "27%.", 27),
 ("To be a small business corporation, a company's gross income for the year may not exceed what amount?", "R20 million.", 20000000),
 ("To be a small business corporation, not more than what percentage of receipts may be investment income and income from personal services?", "20%.", 20),
 ("A taxpayer applying IFRS 9 may deduct what percentage of its lifetime expected credit loss allowance under s11(j)?", "40% (and 25% of the rest of the loss allowance).", 40),
 ("For a bad debt to be deductible under s11(i), what must have happened to the amount in the past?", "It must have been included in the taxpayer's income.", r"income|includ"),
 ("Section 23H does not limit a prepaid expense if the goods or services will be received within how many months after year-end?", "Six months (or if total prepayments are R100 000 or less).", 6),
 ("A restraint of trade payment is deducted under s11(cA) over the restraint period, but over a minimum of how many years?", "Three years.", 3),
 ("A company accrues staff bonuses at year-end and pays them two months later. Can it deduct them in the year of accrual?", "No. Under s7B the employer deducts variable remuneration only when it is paid.", NO + r"|paid"),
 ("Are interest and penalties on late payment of tax deductible?", "No (s23(d)).", NO),
],

# ------------------------------------------------------------------ CGT
"cgt": [
 ("What is the CGT inclusion rate for a company (percent)?", "80%.", 80),
 ("What is the CGT inclusion rate for a natural person (percent)?", "40%.", 40),
 ("What is the annual exclusion in the year a person dies?", "R300 000 (R40 000 in other years).", 300000),
 ("What is the primary residence exclusion?", "R2 million.", 2000000),
 ("An individual sells their primary residence at a capital gain of R2 600 000 and has no other disposals. What is the taxable capital gain?",
  "R224 000: (R2 600 000 - R2 000 000 - R40 000) x 40%.", 224000),
 ("An individual sells their private car at a loss. How is the loss treated for CGT?", "It is disregarded. A private car is a personal-use asset (para 53).", r"^(?!.*\bnot (disregard|exclu|ignor)).*(disregard|exclu|ignor|personal.use|no (capital )?loss|not (allowed|claim|deduct))"),
 ("An asset is donated. What are the proceeds for CGT?", "The market value of the asset on the date of the donation (para 38).", r"market value"),
 ("A capital loss arises on a sale to a connected person. Against what can it be set off?", "Only against capital gains on later disposals to that same connected person (para 39).", r"same|that (connected )?person|clog|ring"),
 ("For the reinvestment relief in paras 65 and 66, the replacement asset must be brought into use within how many years?", "Three years (with the contract concluded within 12 months).", 3),
 ("At what value is a deceased person deemed to dispose of assets on death (other than those left to a surviving spouse)?", "Market value on the date of death (s9HA).", r"market value"),
],

# ------------------------------------------------------------------ Donations tax
"don": [
 ("At what rate is donations tax charged on the first R30 million of cumulative donations (percent)?", "20%. Above R30 million the rate is 25%.", 20),
 ("What is the annual donations tax exemption for a natural person?", "R100 000.", 100000),
 ("A company's casual gifts are exempt from donations tax up to what amount per year?", "R10 000.", 10000),
 ("A donation to a spouse: taxable or exempt?", "Exempt (s56(1)(b)).", r"exempt"),
 ("A donation to an approved public benefit organisation: taxable or exempt?", "Exempt (s56(1)(h)).", r"exempt"),
 ("Who is primarily liable to pay donations tax?", "The donor. If the donor does not pay in time, the donor and donee are jointly liable.", r"donor"),
 ("A natural person donates R400 000 to a friend and makes no other donations in the year. What is the donations tax?", "R60 000: (R400 000 - R100 000) x 20%.", 60000),
 ("A father sells a property with a market value of R1 000 000 to his son for R700 000 and makes no other donations in the year. What is the donations tax?",
  "R40 000. The R300 000 shortfall is a deemed donation (s58); less the R100 000 exemption, at 20%.", 40000),
 ("A donation by a public company: taxable or exempt?", "Exempt (s56(1)(n)).", r"exempt"),
 ("Spouses married in community of property donate an asset from their joint estate. How is the donation attributed?", "Each spouse is treated as having donated half (s57).", r"half|equal|50"),
],

# ------------------------------------------------------------------ Residence & foreign income
"intl": [
 ("Under the physical presence test, a person must be in South Africa for more than how many days in total over the five preceding years?", "915 days.", 915),
 ("Under the physical presence test, a person must be in South Africa for more than how many days in the current year (and in each of the five preceding years)?", "91 days.", 91),
 ("A person who is resident under the physical presence test stops being resident after being outside South Africa for a continuous period of at least how many full days?", "330 full days.", 330),
 ("For the s10(1)(o)(ii) foreign employment exemption, the employee must be outside South Africa for more than how many full days in a 12-month period?", "183 full days, including a continuous period of more than 60 full days.", 183),
 ("The s10(1)(o)(ii) foreign employment exemption is capped at what amount of remuneration per year?", "R1.25 million.", 1250000),
 ("On what income is a South African resident taxed?", "Worldwide income. A non-resident is taxed only on income from a South African source.", r"world|all income|global"),
 ("A foreign dividend is fully exempt if the shareholder holds at least what percentage of the equity shares and voting rights in the foreign company?", "10% (the participation exemption in s10B).", 10),
],

# ------------------------------------------------------------------ Ethics & tax avoidance
"eth": [
 ("Under the general anti-avoidance rule, an arrangement can only be impermissible if its sole or main purpose was to obtain what?", "A tax benefit (s80A).", r"tax benefit"),
 ("A taxpayer deliberately leaves income out of a return. Is this tax avoidance or tax evasion?", "Tax evasion, which is illegal. Avoidance is arranging your affairs within the law to pay less tax.", r"evasion|evad"),
 ("What is the understatement penalty for intentional tax evasion in a standard case (percent)?", "150%.", 150),
 ("How many fundamental principles are in the SAICA Code of Professional Conduct?", "Five: integrity, objectivity, professional competence and due care, confidentiality, and professional behaviour.", 5),
 ("A client asks you to leave income out of their tax return. Which fundamental principle is most directly threatened?", "Integrity.", r"integrity"),
 ("What does NOCLAR stand for?", "Non-compliance with laws and regulations.", [r"non.?compliance", r"law"]),
],
}
