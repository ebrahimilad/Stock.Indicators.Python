from typing import Iterable, List, Optional, Type
from SkenderStockIndicators._cslib import CsIndicator
from SkenderStockIndicators._cstypes import List as CsList
from SkenderStockIndicators._cstypes import Decimal as CsDecimal
from SkenderStockIndicators._cstypes import to_pydecimal
from SkenderStockIndicators.indicators.common.results import IndicatorResults, ResultBase
from SkenderStockIndicators.indicators.common.quote import Quote

def get_adx(quotes: Iterable[Quote], lookback_periods: int = 14):
    adx_results = CsIndicator.GetAdx[Quote](CsList(Quote, quotes), lookback_periods)
    return ADXResults(adx_results, ADXResult)

class ADXResult(ResultBase):
    def __init__(self, adx_result):
        super().__init__(adx_result)

    @property
    def pdi(self):
        return to_pydecimal(self._csdata.Pdi)
    
    @pdi.setter
    def pdi(self, value):
        self._csdata.Pdi = CsDecimal(value)
    
    @property
    def mdi(self):
        return to_pydecimal(self._csdata.Mdi)
    
    @mdi.setter
    def mdi(self, value):
        self._csdata.Mdi = CsDecimal(value)

    @property
    def adx(self):
        return to_pydecimal(self._csdata.Adx)

    @adx.setter
    def adx(self, value):
        self._csdata.Adx = CsDecimal(value)

class ADXResults(IndicatorResults[ADXResult]):
    """
    A wrapper class for the list of ADX results. It is exactly same with built-in `list`
    except for that it provides some useful helper methods written in C# implementation.
    """

    def __init__(self, data: List, wrapper_class: Type[ADXResult]):
        super().__init__(data, wrapper_class)

    @IndicatorResults._verify_data
    def remove_warmup_periods(self, remove_periods: Optional[int] = None):
        if remove_periods is not None:
            return super().remove_warmup_periods(remove_periods)
        
        removed_results = CsIndicator.RemoveWarmupPeriods(CsList(type(self._csdata[0]), self._csdata))

        return self.__class__(removed_results, self._wrapper_class)
        