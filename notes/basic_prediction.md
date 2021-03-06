Running Random Linear Regressions
=================================

## Initial Results (Men)

Method: Take all men's scores. Take scores from before 2017 and call it "history";
        the scores in 2017 will constitute our data set. Take personal best short
        and free scores as a skater's "reputation." For skaters in the 2017
        dataset missing reputation, take the median of all reputation values. We
        normalize start numbers to be between 0 and 1; a higher start number is a
        later skate (which we hypothesize to have a positive effect on scores).

Model: segment_score = segment_reputation + start_order
            (separately for short and free, because otherwise response variable is
             clearly not normal)

### Code to Make Vectors
```
individual_bests_short = {skater: np.max(map(float, history[history.Name == skater]['Short Score']))
                          for skater in history.Name.get_values()}

have_frees = history[history['Free Rank'] != 'DNQ']
have_frees = have_frees[have_frees['Free Rank'] != 'WD']
individual_bests_free = {skater: np.max(map(float, have_frees[have_frees.Name == skater]['Free Score']))
                         for skater in have_frees.Name.get_values()}

med_short = np.median(individual_bests_short.values())
med_free = np.median(individual_bests_free.values())

start = []        # normalized start order b/w 0 and 1, closer to 1 is later
reputation = []   # maximum of historical total scores. if no history, then median of existing skaters'
score = []
skaters_short = []

start_free = []
reputation_free = []
score_free = []
skaters_free = []

for idx, row in start_order17.iterrows():
    start.append(row.loc['Short Start'] / float(row.loc['Num Short Scorecards']))
    if row.Name in individual_bests_short:
        reputation.append(individual_bests_short[row.Name])
    else:
        reputation.append(med_short)
    score.append(row.loc['Short Score'])
    skaters_short.append(row.loc['Name'])
    
    if pd.notnull(row.loc['Free Start']):
        start_free.append(row.loc['Free Start'] /  float(row.loc['Num Free Scorecards']))
        if row.Name in individual_bests_free:
            reputation_free.append(individual_bests_free[row.Name])
        else:
            reputation_free.append(med_free)
        score_free.append(row.loc['Free Score'])
        skaters_free.append(row.loc['Name'])

# Model: short_score = reputation + start_order
X = pd.DataFrame({'Reputation': reputation, 'Start Number': start}).astype(float)
X = sm.add_constant(X)
y_short = pd.Series(score).astype(float)
mod_short = sm.OLS(y_short, X).fit()
print mod_short.summary()
```

### Short Program
170 data points, 76 skaters
```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.617
Model:                            OLS   Adj. R-squared:                  0.612
Method:                 Least Squares   F-statistic:                     134.4
Date:                Thu, 01 Feb 2018   Prob (F-statistic):           1.63e-35
Time:                        23:54:42   Log-Likelihood:                -614.99
No. Observations:                 170   AIC:                             1236.
Df Residuals:                     167   BIC:                             1245.
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [95.0% Conf. Int.]
--------------------------------------------------------------------------------
const           20.8236      3.619      5.754      0.000        13.679    27.968
Reputation       0.6155      0.051     11.991      0.000         0.514     0.717
Start Number    12.3222      2.710      4.546      0.000         6.971    17.673
==============================================================================
Omnibus:                       16.378   Durbin-Watson:                   1.627
Prob(Omnibus):                  0.000   Jarque-Bera (JB):               37.143
Skew:                           0.374   Prob(JB):                     8.60e-09
Kurtosis:                       5.164   Cond. No.                         411.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```


### Free Program
144 data points, 62 skaters

```
OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.583
Model:                            OLS   Adj. R-squared:                  0.577
Method:                 Least Squares   F-statistic:                     98.40
Date:                Thu, 01 Feb 2018   Prob (F-statistic):           1.78e-27
Time:                        23:54:54   Log-Likelihood:                -607.37
No. Observations:                 144   AIC:                             1221.
Df Residuals:                     141   BIC:                             1230.
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [95.0% Conf. Int.]
--------------------------------------------------------------------------------
const           72.3915      7.850      9.222      0.000        56.873    87.910
Reputation       0.3983      0.058      6.918      0.000         0.284     0.512
Start Number    35.2871      5.862      6.020      0.000        23.699    46.875
==============================================================================
Omnibus:                        9.173   Durbin-Watson:                   1.495
Prob(Omnibus):                  0.010   Jarque-Bera (JB):               12.356
Skew:                           0.368   Prob(JB):                      0.00207
Kurtosis:                       4.232   Cond. No.                         945.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

### Comments
* Start number is very significant. The coefficient is large because the indicator
  is between 0 and 1.
* Skaters tend to earn at least 60% of their short PB and 40% of their free PB. (Note
  again that "Reputation" is different in both regressions, since they're separated
  by program to account for someone being better/worse at a program.)
* Start number is much more significant in the free. Possible explanations:
  * The free program tends to be more seeded than the short program. Seeding for the
      short varies by competition, whereas the free order always depends on SP
      placements.
  * The free generally has higher variability, and it's easier to completely lose it.
      Then skaters are less likely to achieve PBs and then the influence skews towards
      start order.
* This does not take consistency into account at all? R-squared are each about 0.6.
* Outliers in the short: Nathan Chen (LOL in 2017), Daniel Samohin's terrible short



## Pairs

### Short
```
OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.509
Model:                            OLS   Adj. R-squared:                  0.500
Method:                 Least Squares   F-statistic:                     55.91
Date:                Mon, 05 Feb 2018   Prob (F-statistic):           2.15e-17
Time:                        14:40:25   Log-Likelihood:                -374.28
No. Observations:                 111   AIC:                             754.6
Df Residuals:                     108   BIC:                             762.7
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [95.0% Conf. Int.]
--------------------------------------------------------------------------------
const           26.6549      4.185      6.369      0.000        18.360    34.950
Reputation       0.5133      0.077      6.677      0.000         0.361     0.666
Start Number    10.4161      2.704      3.852      0.000         5.056    15.777
==============================================================================
Omnibus:                        3.837   Durbin-Watson:                   1.470
Prob(Omnibus):                  0.147   Jarque-Bera (JB):                3.750
Skew:                           0.447   Prob(JB):                        0.153
Kurtosis:                       2.888   Cond. No.                         383.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
* No real outliers, but Xiaoyu YU / Hao ZHANG are the smallest p-value


### Free
```
OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.656
Model:                            OLS   Adj. R-squared:                  0.649
Method:                 Least Squares   F-statistic:                     89.61
Date:                Mon, 05 Feb 2018   Prob (F-statistic):           1.66e-22
Time:                        14:42:04   Log-Likelihood:                -359.70
No. Observations:                  97   AIC:                             725.4
Df Residuals:                      94   BIC:                             733.1
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [95.0% Conf. Int.]
--------------------------------------------------------------------------------
const           57.2884      6.361      9.007      0.000        44.659    69.917
Reputation       0.3892      0.060      6.504      0.000         0.270     0.508
Start Number    28.9112      4.027      7.179      0.000        20.915    36.907
==============================================================================
Omnibus:                        0.552   Durbin-Watson:                   1.439
Prob(Omnibus):                  0.759   Jarque-Bera (JB):                0.256
Skew:                          -0.111   Prob(JB):                        0.880
Kurtosis:                       3.119   Cond. No.                         752.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

* Outliers: ('Evgenia TARASOVA / Vladimir MOROZOV', '110.7') at gpusa2016 (bad)
* Note: pairs scores aren't as normally distributed as men's


## Model: Two Previous Scores
```
segment score = last segment score + last last segment score
                    (if missing data, 0.)
```
* Low R-squared.

Then plus start order again:
```
segment score = last segment score + last last segment score + normalized start order
```
* Bumps R-squared up to about 0.5.

Then Plus Reputation Again:
```
segment score = last segment score + last last segment score + normalized start order + reputation
```
* As expected there are collinearity problems, prev scores become unimportant.



## NEXT STEPS
Choices:
* read about some different models
* get the 2018 data and test these models on them
* start diving into details (will have to brainstorm)



## MED TES + MAX PCS
(Pairs)

### Short
```
 OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.522
Model:                            OLS   Adj. R-squared:                  0.508
Method:                 Least Squares   F-statistic:                     38.91
Date:                Mon, 05 Feb 2018   Prob (F-statistic):           4.39e-17
Time:                        20:05:43   Log-Likelihood:                -372.78
No. Observations:                 111   AIC:                             753.6
Df Residuals:                     107   BIC:                             764.4
Df Model:                           3                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [95.0% Conf. Int.]
--------------------------------------------------------------------------------
const           26.7677      4.889      5.475      0.000        17.076    36.459
Avg TES         -0.6253      0.534     -1.170      0.244        -1.684     0.434
Max PCS          1.9460      0.591      3.293      0.001         0.775     3.117
Start Number     9.7409      2.717      3.585      0.001         4.354    15.128
==============================================================================
Omnibus:                        2.493   Durbin-Watson:                   1.504
Prob(Omnibus):                  0.288   Jarque-Bera (JB):                2.338
Skew:                           0.354   Prob(JB):                        0.311
Kurtosis:                       2.931   Cond. No.                         297.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
* Increased R^2 from just reputation + start order. Interpretation could be that
  max PCS = reputation.
* No reported outliers.

### Free
```
OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.647
Model:                            OLS   Adj. R-squared:                  0.636
Method:                 Least Squares   F-statistic:                     56.94
Date:                Mon, 05 Feb 2018   Prob (F-statistic):           5.52e-21
Time:                        20:06:00   Log-Likelihood:                -360.88
No. Observations:                  97   AIC:                             729.8
Df Residuals:                      93   BIC:                             740.1
Df Model:                           3                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [95.0% Conf. Int.]
--------------------------------------------------------------------------------
const           46.3368      8.717      5.315      0.000        29.026    63.648
Avg TES          0.6316      0.345      1.833      0.070        -0.053     1.316
Max PCS          0.3979      0.294      1.353      0.179        -0.186     0.982
Start Number    29.4558      4.104      7.177      0.000        21.306    37.605
==============================================================================
Omnibus:                        1.724   Durbin-Watson:                   1.414
Prob(Omnibus):                  0.422   Jarque-Bera (JB):                1.172
Skew:                          -0.225   Prob(JB):                        0.557
Kurtosis:                       3.297   Cond. No.                         661.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
* Actually decreased R^2 from just reputation + start order, and neither TES nor
  PCS shows up as significant.
* Tarasova/Morozov gpusa free is again an outlier due to an unexpectedly bad performance.

### Notes
* If you remove start number from both models, TES is not significant but PCS is.
* "Reputation" as median TES + max PCS gives a similar (but actually worse) model
  to our original reputation + start order model.


## Start Order + Reputation for Ladies
Note: normality is decent.

### Short
72 skaters, 169 data points
```
                            OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.446
Model:                            OLS   Adj. R-squared:                  0.439
Method:                 Least Squares   F-statistic:                     66.82
Date:                Sun, 25 Feb 2018   Prob (F-statistic):           5.16e-22
Time:                        21:06:37   Log-Likelihood:                -585.08
No. Observations:                 169   AIC:                             1176.
Df Residuals:                     166   BIC:                             1186.
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [95.0% Conf. Int.]
--------------------------------------------------------------------------------
const           21.8275      3.362      6.492      0.000        15.189    28.466
Reputation       0.5289      0.058      9.160      0.000         0.415     0.643
Start Number    10.5243      2.123      4.957      0.000         6.332    14.716
==============================================================================
Omnibus:                        0.037   Durbin-Watson:                   1.283
Prob(Omnibus):                  0.982   Jarque-Bera (JB):                0.151
Skew:                           0.018   Prob(JB):                        0.927
Kurtosis:                       2.858   Cond. No.                         334.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
No outliers detected.

### Free
60 skaters, 144 data points

```
OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.486
Model:                            OLS   Adj. R-squared:                  0.479
Method:                 Least Squares   F-statistic:                     66.68
Date:                Sun, 25 Feb 2018   Prob (F-statistic):           4.15e-21
Time:                        21:11:35   Log-Likelihood:                -567.07
No. Observations:                 144   AIC:                             1140.
Df Residuals:                     141   BIC:                             1149.
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [95.0% Conf. Int.]
--------------------------------------------------------------------------------
const           71.8259      6.684     10.746      0.000        58.612    85.040
Reputation       0.1939      0.062      3.116      0.002         0.071     0.317
Start Number    35.1033      3.867      9.078      0.000        27.459    42.748
==============================================================================
Omnibus:                       12.270   Durbin-Watson:                   1.454
Prob(Omnibus):                  0.002   Jarque-Bera (JB):               16.509
Skew:                          -0.498   Prob(JB):                     0.000260
Kurtosis:                       4.326   Cond. No.                         742.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```
* Interesting that reputation's p-value is larger.
* Outlier: ('Julia LIPNITSKAIA', '78.88') her terrible showing at gprus2016 


## Dance
### Short
57 skaters, 142 data points

```
OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.817
Model:                            OLS   Adj. R-squared:                  0.815
Method:                 Least Squares   F-statistic:                     310.9
Date:                Thu, 15 Mar 2018   Prob (F-statistic):           4.93e-52
Time:                        13:12:38   Log-Likelihood:                -421.20
No. Observations:                 142   AIC:                             848.4
Df Residuals:                     139   BIC:                             857.3
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
const           11.1460      2.121      5.256      0.000       6.953      15.339
Reputation       0.8128      0.040     20.553      0.000       0.735       0.891
Start Number     3.8923      1.545      2.519      0.013       0.837       6.947
==============================================================================
Omnibus:                        7.773   Durbin-Watson:                   1.473
Prob(Omnibus):                  0.021   Jarque-Bera (JB):               11.200
Skew:                           0.269   Prob(JB):                      0.00370
Kurtosis:                       4.266   Cond. No.                         326.
==============================================================================

Warnings:
[1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
```

Outliers (no appearances prior to 2016-2017):
* Tiffany ZAHORSKI / Jonathan GUERREIRO: 64.28, 0.002527
* Elliana POGREBINSKY / Alex BENOIT: 62.93, 0.001319
* Kimberley HEW-LOW / Timothy MCKERNAN: 33.54, 0.001835
* Olivia SMART / Adria DIAZ: 60.93, 0.004997

### Free
46 skaters, 120 data points

```
OLS Regression Results                            
==============================================================================
Dep. Variable:                      y   R-squared:                       0.828
Model:                            OLS   Adj. R-squared:                  0.825
Method:                 Least Squares   F-statistic:                     280.8
Date:                Thu, 15 Mar 2018   Prob (F-statistic):           2.18e-45
Time:                        13:24:46   Log-Likelihood:                -385.33
No. Observations:                 120   AIC:                             776.7
Df Residuals:                     117   BIC:                             785.0
Df Model:                           2                                         
Covariance Type:            nonrobust                                         
================================================================================
                   coef    std err          t      P>|t|      [0.025      0.975]
--------------------------------------------------------------------------------
const           21.5212      4.946      4.351      0.000      11.725      31.317
Reputation       0.7030      0.065     10.780      0.000       0.574       0.832
Start Number    12.6694      3.234      3.917      0.000       6.264      19.075
==============================================================================
Omnibus:                       39.545   Durbin-Watson:                   1.767
Prob(Omnibus):                  0.000   Jarque-Bera (JB):              108.904
Skew:                          -1.217   Prob(JB):                     2.25e-24
Kurtosis:                       6.981   Cond. No.                         951.
==============================================================================
```

Outliers are unobserved previously, lower free dance score than median of 78.62:
* Adele MORRISON / Demid ROKACHEV 58.48
* Kimberley HEW-LOW / Timothy MCKERNAN 51.43