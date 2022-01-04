from tslearn.bases import TimeSeriesBaseEstimator
import numpy
from sklearn.base import TransformerMixin
from sklearn.utils import check_array
from sklearn.utils.validation import check_is_fitted

class TimeSeriesScalerMinMax(TransformerMixin, TimeSeriesBaseEstimator):
    """Scaler for time series. Scales time series so that their span in each
    dimension is between ``min`` and ``max`` where ``value_range=(min, max)``.
    Parameters
    ----------
    value_range : tuple (default: (0., 1.))
        The minimum and maximum value for the output time series.
    Notes
    -----
        This method requires a dataset of equal-sized time series.
        NaNs within a time series are ignored when calculating min and max.
    Examples
    --------
    >>> TimeSeriesScalerMinMax(value_range=(1., 2.)).fit_transform([[0, 3, 6]])
    array([[[1. ],
            [1.5],
            [2. ]]])
    >>> TimeSeriesScalerMinMax(value_range=(1., 2.)).fit_transform(
    ...     [[numpy.nan, 3, 6]]
    ... )
    array([[[nan],
            [ 1.],
            [ 2.]]])
    """
    def __init__(self, value_range=(0., 1.)):
        self.value_range = value_range

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
        """Will normalize (min-max) each of the timeseries. IMPORTANT: this
        transformation is completely stateless, and is applied to each of
        the timeseries individually.
        Parameters
        ----------
        X : array-like of shape (n_ts, sz, d)
            Time series dataset to be rescaled.
        Returns
        -------
        numpy.ndarray
            Rescaled time series dataset.
        """
        value_range = self.value_range

        if value_range[0] >= value_range[1]:
            raise ValueError("Minimum of desired range must be smaller"
                             " than maximum. Got %s." % str(value_range))

        check_is_fitted(self, '_X_fit_dims')
        X = check_array(X, allow_nd=True, force_all_finite=False)
        X_ = to_time_series_dataset(X)
        X_ = check_dims(X_, X_fit_dims=self._X_fit_dims, extend=False)
        min_t = numpy.nanmin(X_, axis=1)[:, numpy.newaxis, :]
        max_t = numpy.nanmax(X_, axis=1)[:, numpy.newaxis, :]
        range_t = max_t - min_t
        range_t[range_t == 0.] = 1.
        nomin = (X_ - min_t) * (value_range[1] - value_range[0])
        X_ = nomin / range_t + value_range[0]
        return X_, min_t, max_t, range_t

    def _more_tags(self):
        return {'allow_nan': True}