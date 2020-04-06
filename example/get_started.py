#! /bin/python3
# vim: set expandtab:
# -------------------------------------------------------------------------
import sys
import pandas as pd
import numpy as np 
import curvefit
#
# -------------------------------------------------------------------------
# load NYC data
nycdf = pd.read_csv('~/Dev/exp-modelling/data/ny_google.csv')
nycdf['day'] = pd.Series([i+1 for i in range(len(nycdf))])
# set vars
n_data       = len(nycdf) # 29
num_params   = 3 # alpha beta p
alpha_true   = 2.0
beta_true    = 3.0
p_true       = 4.0
rel_tol      = 1e-6
# -------------------------------------------------------------------------
# model for the mean of the data
def generalized_logistic(t, params) :
    alpha = params[0]
    beta  = params[1]
    p     = params[2]
    return p / ( 1.0 + np.exp( - alpha * ( t - beta ) ) )
#
# link function used for beta
def identity_fun(x) :
    return x
#
# link function used for alpha, p
def exp_fun(x) :
    return np.exp(x)
#
# params_true
params_true       = np.array( [ alpha_true, beta_true, p_true ] )
#


# data_frame
independent_var   = nycdf['day']
measurement_value = nycdf['cases'] # generalized_logistic(independent_var, params_true)
measurement_std   = n_data * [ 0.1 ] # NEED TO DEFINE, SET TO NONE FOR NOW BELOW

    # covariates
deaths            = nycdf['deaths'] # ['deaths', 'isolations', 'icu']
# isolations        = nycdf['isolations'] # ['deaths', 'isolations', 'icu']
# hospitalizations  = nycdf['hospitalizations'] # ['deaths', 'isolations', 'icu']

data_group        = nycdf['fips']

data_dict         = {
    'independent_var'   : independent_var   ,
    'measurement_value' : measurement_value ,
    'measurement_std'   : measurement_std   ,
    'deaths'              : deaths      ,
    'region'            : data_group        ,
}
data_frame        = pd.DataFrame(data_dict)
#
# curve_model
col_t        = 'independent_var'
col_obs      = 'measurement_value'
col_covs     = num_params *[ [ 'deaths' ] ]
col_group    = 'region'
param_names  = [ 'alpha', 'beta',       'p'     ]
link_fun     = [ exp_fun, identity_fun, exp_fun ]
var_link_fun = link_fun
fun          = generalized_logistic
col_obs_se   = None # 'measurement_std'
#
curve_model = curvefit.CurveModel(
    data_frame,
    col_t,
    col_obs,
    col_covs,
    col_group,
    param_names,
    link_fun,
    var_link_fun,
    fun,
    col_obs_se
)
#
# fit_params
# TODO: what do do about the below line when we don't have params true?
fe_init         = params_true / 3.0
curve_model.fit_params(fe_init)
params_estimate = curve_model.params
#
# for i in range(num_params) :
#     rel_error = params_estimate[i] / params_true[i] - 1.0
#     assert abs(rel_error) < rel_tol
#
print(params_estimate)
print('get_started.py: OK')
sys.exit(0)
