#!/usr/bin/env python
    # -*- coding: utf-8 -*-
    #
    # yfinance - market data downloader
    # https://github.com/ranaroussi/yfinance
    #
    # Copyright 2017-2019 Ran Aroussi
    #
    # Licensed under the Apache License, Version 2.0 (the "License");
    # you may not use this file except in compliance with the License.
    # You may obtain a copy of the License at
    #
    #     http://www.apache.org/licenses/LICENSE-2.0
    #
    # Unless required by applicable law or agreed to in writing, software
    # distributed under the License is distributed on an "AS IS" BASIS,
    # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    # See the License for the specific language governing permissions and
    # limitations under the License.
    #

    from __future__ import print_function

    from io import StringIO
    import json as _json
    import warnings
    from typing import Optional, Union
    from urllib.parse import quote as urlencode

    import pandas as pd
    import requests

    from . import utils, cache
    from .data import YfData
    from .exceptions import YFEarningsDateMissing
    from .scrapers.analysis import Analysis
    from .scrapers.fundamentals import Fundamentals
    from .scrapers.holders import Holders
    from .scrapers.quote import Quote, FastInfo
    from .scrapers.history import PriceHistory
    from .scrapers.funds import FundsData

    from .const import _BASE_URL_, _ROOT_URL_


    class TickerBase:
        def __init__(self, ticker, session=None, proxy=None):
            self.ticker = ticker.upper()
            self.proxy = proxy
            self.session = session
            self._tz = None

            self._isin = None
            self._news = []
            self._shares = None

            self._earnings_dates = {}

            self._earnings = None
            self._financials = None

            # accept isin as ticker
            if utils.is_isin(self.ticker):
                self.ticker = utils.get_ticker_by_isin(self.ticker, None, session)

            self._data: YfData = YfData(session=session)

            # self._price_history = PriceHistory(self._data, self.ticker)
            self._price_history = None  # lazy-load
            self._analysis = Analysis(self._data, self.ticker)
            self._holders = Holders(self._data, self.ticker)
            self._quote = Quote(self._data, self.ticker)
            self._fundamentals = Fundamentals(self._data, self.ticker)
            self._funds_data = None

            self._fast_info = None

        @utils.log_indent_decorator
        def history(self, *args, **kwargs) -> pd.DataFrame:
            return self._lazy_load_price_history().history(*args, **kwargs)

        # ------------------------

        def _lazy_load_price_history(self):
            if self._price_history is None:
                self._price_history = PriceHistory(self._data, self.ticker, self._get_ticker_tz(self.proxy, timeout=10))
            return self._price_history

        def _get_ticker_tz(self, proxy, timeout):
            proxy = proxy or self.proxy
            if self._tz is not None:
                return self._tz
            c = cache.get_tz_cache()
            tz = c.lookup(self.ticker)

            if tz and not utils.is_valid_timezone(tz):
                # Clear from cache and force re-fetch
                c.store(self.ticker, None)
                tz = None

            if tz is None:
                tz = self._fetch_ticker_tz(proxy, timeout)

                if utils.is_valid_timezone(tz):
                    # info fetch is relatively slow so cache timezone
                    c.store(self.ticker, tz)
                else:
                    tz = None

            self._tz = tz
            return tz

        @utils.log_indent_decorator
        def _fetch_ticker_tz(self, proxy, timeout):
            # Query Yahoo for fast price data just to get returned timezone
            proxy = proxy or self.proxy
            logger = utils.get_yf_logger()

            params = {"range": "1d", "interval": "1d"}

            # Getting data from json
            url = f"{_BASE_URL_}/v8/finance/chart/{self.ticker}"

            try:
                data = self._data.cache_get(url=url, params=params, proxy=proxy, timeout=timeout)
                data = data.json()
            except Exception as e:
                logger.error(f"Failed to get ticker '{self.ticker}' reason: {e}")
                return None
            else:
                error = data.get('chart', {}).get('error', None)
                if error:
                    # explicit error from yahoo API
                    logger.debug(f"Got error from yahoo api for ticker {self.ticker}, Error: {error}")
                else:
                    try:
                        return data["chart"]["result"][0]["meta"]["exchangeTimezoneName"]
                    except Exception as err:
                        logger.error(f"Could not get exchangeTimezoneName for ticker '{self.ticker}' reason: {err}")
                        logger.debug("Got response: ")
                        logger.debug("-------------")
                        logger.debug(f" {data}")
                        logger.debug("-------------")
            return None

        def get_recommendations(self, proxy=None, as_dict=False):
            """
            Returns a DataFrame with the recommendations
            Columns: period  strongBuy  buy  hold  sell  strongSell
            """
            self._quote.proxy = proxy or self.proxy
            data = self._quote.recommendations
            if as_dict:
                return data.to_dict()
            return data

        def get_recommendations_summary(self, proxy=None, as_dict=False):
            return self.get_recommendations(proxy=proxy, as_dict=as_dict)

        def get_upgrades_downgrades(self, proxy=None, as_dict=False):
            """
            Returns a DataFrame with the recommendations changes (upgrades/downgrades)
            Index: date of grade
            Columns: firm toGrade fromGrade action
            """
            self._quote.proxy = proxy or self.proxy
            data = self._quote.upgrades_downgrades
            if as_dict:
                return data.to_dict()
            return data

        def get_calendar(self, proxy=None) -> dict:
            self._quote.proxy = proxy or self.proxy
            return self._quote.calendar

        def get_sec_filings(self, proxy=None) -> dict:
            self._quote.proxy = proxy or self.proxy
            return self._quote.sec_filings

        def get_major_holders(self, proxy=None, as_dict=False):
            self._holders.proxy = proxy or self.proxy
            data = self._holders.major
            if as_dict:
                return data.to_dict()
            return data

        def get_institutional_holders(self, proxy=None, as_dict=False):
            self._holders.proxy = proxy or self.proxy
            data = self._holders.institutional
            if data is not None:
                if as_dict:
                    return data.to_dict()
                return data

        def get_mutualfund_holders(self, proxy=None, as_dict=False):
            self._holders.proxy = proxy or self.proxy
            data = self._holders.mutualfund
            if data is not None:
                if as_dict:
                    return data.to_dict()
                return data

        def get_insider_purchases(self, proxy=None, as_dict=False):
            self._holders.proxy = proxy or self.proxy
            data = self._holders.insider_purchases
            if data is not None:
                if as_dict:
                    return data.to_dict()
                return data

        def get_insider_transactions(self, proxy=None, as_dict=False):
            self._holders.proxy = proxy or self.proxy
            data = self._holders.insider_transactions
            if data is not None:
                if as_dict:
                    return data.to_dict()
                return data
