# -------------------------------------------------------------------------------------------------
# <copyright file="brokerage.pxd" company="Nautech Systems Pty Ltd">
#  Copyright (C) 2015-2019 Nautech Systems Pty Ltd. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  https://nautechsystems.io
# </copyright>
# -------------------------------------------------------------------------------------------------

from nautilus_trader.model.objects cimport Money, Quantity, Price
from nautilus_trader.model.identifiers cimport Symbol


cdef class CommissionCalculator:
    """
    Provides a means of calculating commissions.
    """
    cdef dict rates
    cdef float default_rate_bp
    cdef Money minimum

    cpdef Money calculate(self, Symbol symbol, Quantity filled_quantity, Price filled_price, float exchange_rate)
    cpdef Money calculate_for_notional(self, Symbol symbol, Money notional_value)

    cdef float _get_commission_rate(self, Symbol symbol)
