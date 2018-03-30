TODO
====

### 3/23 Meeting with Jim
* Make code available and see if I can put the data in the repo. Should be a
  little cleaner but doesn't have to be beautiful.
* Literature review just has to prove that you're doing something that hasn't
  been done in this way before.
* Should cite all data source links (woohoo bibliography is getting bigger).
* Write bias chapter by Saturday, he will look at it over the weekend.

### Todo 3/12
Options
* start bias stuff
* continue prediction
  * hts
  * apply model to pairs + dance
  * look into tennis + golf ranking systems as inspiration


### 3/9 Meeting
* overview of what I've done to this point
  * I haven't gotten any model to beat OLS on both metrics yet
  * I'm looking into time series, but I really don't have good data unless
    I do some sort of hierarchical time series stuff, which I'm investigating
    in R right now.
* I realize prediction without many predictors is hard (hence the time series
  route)
  * I want to try something simple like create a ranking system based on
    observations
    * tennis and golf?
  * Alternatively could do a section on asking historical questions as well
    * when does the judges' score break from my linear regression predictions
* What to do for spring break
  * Should I start writing?

### 2/25
* build prediction2.5, which improves score loss but rank loss gets worse
* test prediction 2 and prediction 2.5 on ladies. expectedly bad because
  it didn't know Alina Zagitova was coming.

### 2/24
* build prediction2, which performs strictly worse than OLS
* tbh I think the most accurate components prediction is going to be the last
  observed ones
* improvements to make:
    * add predictors
    * weight recent results more heavily
    * improve element grouping + assumptions

### 2/11 Weekend
* Build a predictive model
  * points distribution over each kind of element for each skater
  * components modeled on historical components scores
  * then add it all up

### Monday 2/5
* ran regressions on pairs
* made BS predictions based on last two performances

### Sunday 2/4
* fixed pairs, dance, ladies' names
* found Nathan Chen + Daniel Samohin as outliers in 2017