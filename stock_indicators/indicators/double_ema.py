from decimal import Decimal
from typing import Iterable, Optional, TypeVar
from stock_indicators._cslib import CsIndicator
from stock_indicators._cstypes import List as CsList
from stock_indicators._cstypes import Decimal as CsDecimal
from stock_indicators._cstypes import to_pydecimal
from stock_indicators.indicators.common.results import IndicatorResults, ResultBase
from stock_indicators.indicators.common.quote import Quote

def get_double_ema(quotes: Iterable[Quote], lookback_periods: int):
    """Get DEMA calculated.
    
    Double Exponential Moving Average (DEMA) of the Close price.
    
    Parameters:
        `quotes` : Iterable[Quotes]
            Historical price quotes.
        
        `lookback_periods` : int
            Number of periods in the lookback window.
    
    Returns:
        `DEMAResults[DEMAResult]`
            DEMAResults is list of DEMAResult with providing useful helper methods.
    
    See more:
         - [DEMA Reference](https://daveskender.github.io/Stock.Indicators.Python/indicators/DoubleEma/#content)
         - [Helper Methods](https://daveskender.github.io/Stock.Indicators.Python/utilities/#content)
    """
    results = CsIndicator.GetDoubleEma[Quote](CsList(Quote, quotes), lookback_periods)
    return DEMAResults(results, DEMAResult)

class DEMAResult(ResultBase):
    """
    A wrapper class for a single unit of Double Exponential Moving Average (DEMA) results.
    """

    @property
    def dema(self) -> Optional[Decimal]:
        return to_pydecimal(self._csdata.Dema)

    @dema.setter
    def dema(self, value):
        self._csdata.Dema = CsDecimal(value)

T = TypeVar("T", bound=DEMAResult)
class DEMAResults(IndicatorResults[T]):
    """
    A wrapper class for the list of Double Exponential Moving Average (DEMA) results.
    It is exactly same with built-in `list` except for that it provides
    some useful helper methods written in C# implementation.
    """

    @IndicatorResults._verify_data
    def remove_warmup_periods(self, remove_periods: Optional[int] = None):
        if remove_periods is not None:
            return super().remove_warmup_periods(remove_periods)

        removed_results = CsIndicator.RemoveWarmupPeriods(CsList(type(self._csdata[0]), self._csdata))

        return self.__class__(removed_results, self._wrapper_class)
        