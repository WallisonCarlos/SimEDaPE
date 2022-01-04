from tslearn.bases import TimeSeriesBaseEstimator
import numpy
from sklearn.base import TransformerMixin
from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted
from tslearn.utils import (to_time_series_dataset, check_equal_size, ts_size,
                           check_dims)

class TimeSeriesScalerSimEDaPE(TransformerMixin, TimeSeriesBaseEstimator):
    """Scaler for time series. Scales time series so that their mean (resp.
    standard deviation) in each dimension is
    mu (resp. std).
    Parameters
    ----------
    mu : float (default: 0.)
        Mean of the output time series.
    std : float (default: 1.)
        Standard deviation of the output time series.
    Notes
    -----
        This method requires a dataset of equal-sized time series.
        NaNs within a time series are ignored when calculating mu and std.
    Examples
    --------
    >>> TimeSeriesScalerMeanVariance(mu=0.,
    ...                              std=1.).fit_transform([[0, 3, 6]])
    array([[[-1.22474487],
            [ 0.        ],
            [ 1.22474487]]])
    >>> TimeSeriesScalerMeanVariance(mu=0.,
    ...                              std=1.).fit_transform([[numpy.nan, 3, 6]])
    array([[[nan],
            [-1.],
            [ 1.]]])
    """
    
    def __init__(self, mu=0., std=1.):
        self.mu = mu
        self.std = std

    def fit(self, X, y=None, **kwargs):
        """A dummy method such that it complies to the sklearn requirements.
        Since this method is completely stateless, it just returns itself.
        Parameters
        ----------
        X
            Ignored
        Returns
        -------
        self
        """
        X = check_array(X, allow_nd=True, force_all_finite=False)
        X = to_time_series_dataset(X)
        self._X_fit_dims = X.shape
        return self

    def fit_transform(self, X, y=None, **kwargs):
        """Fit to data, then transform it.
        Parameters
        ----------
        X : array-like of shape (n_ts, sz, d)
            Time series dataset to be rescaled.
        Returns
        -------
        numpy.ndarray
            Resampled time series dataset.
        """
        return self.fit(X).transform(X)

    def transform(self, X, y=None, **kwargs):
        """Fit to data, then transform it.
        Parameters
        ----------
        X : array-like of shape (n_ts, sz, d
    i,)
            Time series dataset to be rescaled
        Returns
        -------
        numpy.ndarray
            Rescaled time series dataset
        """
        check_is_fitted(self, '_X_fit_dims')
        X = check_array(X, allow_nd=True, force_all_finite=False)
        X_ = to_time_series_dataset(X)
        X_ = check_dims(X_, X_fit_dims=self._X_fit_dims, extend=False)
        mean_t = numpy.nanmean(X_, axis=1, keepdims=True)
        std_t = numpy.nanstd(X_, axis=1, keepdims=True)
        std_t[std_t == 0.] = 1.
        X_ = (X_ - mean_t) * self.std / std_t + self.mu

        return X_, mean_t, std_t

    def _more_tags(self):
        return {'allow_nan': True}