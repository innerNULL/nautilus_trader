#!/usr/bin/env python3
# -------------------------------------------------------------------------------------------------
# <copyright file="test_account.py" company="Invariance Pte">
#  Copyright (C) 2018-2019 Invariance Pte. All rights reserved.
#  The use of this source code is governed by the license as found in the LICENSE.md file.
#  http://www.invariance.com
# </copyright>
# -------------------------------------------------------------------------------------------------

import unittest
import uuid

from inv_trader.model.enums import Broker, CurrencyCode
from inv_trader.model.account import Account
from inv_trader.model.events import AccountEvent
from inv_trader.model.identifiers import AccountId, AccountNumber
from inv_trader.model.objects import Money
from test_kit.stubs import TestStubs

UNIX_EPOCH = TestStubs.unix_epoch()


class AccountTests(unittest.TestCase):

    def test_can_initialize_account_with_event(self):
        # Arrange
        account = Account()

        event = AccountEvent(
            AccountId('FXCM-D102412895'),
            Broker.FXCM,
            AccountNumber('D102412895'),
            CurrencyCode.AUD,
            Money.create(100000.00),
            Money.create(100000.00),
            Money.zero(),
            Money.zero(),
            Money.zero(),
            Money.zero(),
            "",
            uuid.uuid4(),
            UNIX_EPOCH)

        # Act
        account.apply(event)

        # Assert
        self.assertTrue(account.initialized)
        self.assertEqual(AccountId('FXCM-D102412895'), account.id)
        self.assertEqual(Broker.FXCM, account.broker)
        self.assertEqual(AccountNumber('D102412895'), account.number)
        self.assertEqual(CurrencyCode.AUD, account.currency)
        self.assertEqual(Money.create(100000), account.free_equity)
        self.assertEqual(Money.create(100000), account.cash_start_day)
        self.assertEqual(Money.zero(), account.cash_activity_day)
        self.assertEqual(Money.zero(), account.margin_used_liquidation)
        self.assertEqual(Money.zero(), account.margin_used_maintenance)
        self.assertEqual(Money.zero(), account.margin_ratio)
        self.assertEqual("", account.margin_call_status)
        self.assertEqual(UNIX_EPOCH, account.last_updated)

    def test_can_calculate_free_equity(self):
        # Arrange
        account = Account()

        event = AccountEvent(
            AccountId('FXCM-D102412895'),
            Broker.FXCM,
            AccountNumber('D102412895'),
            CurrencyCode.AUD,
            Money.create(100000.00),
            Money.create(100000.00),
            Money.zero(),
            Money.create(1000.00),
            Money.create(2000.00),
            Money.zero(),
            "",
            uuid.uuid4(),
            UNIX_EPOCH)

        # Act
        account.apply(event)

        # Assert
        self.assertTrue(account.initialized)
        self.assertEqual(AccountId('FXCM-D102412895'), account.id)
        self.assertEqual(Broker.FXCM, account.broker)
        self.assertEqual(AccountNumber('D102412895'), account.number)
        self.assertEqual(CurrencyCode.AUD, account.currency)
        self.assertEqual(Money.create(97000.00), account.free_equity)
        self.assertEqual(Money.create(100000.00), account.cash_start_day)
        self.assertEqual(Money.zero(), account.cash_activity_day)
        self.assertEqual(Money.create(1000.00), account.margin_used_liquidation)
        self.assertEqual(Money.create(2000.00), account.margin_used_maintenance)
        self.assertEqual(Money.zero(), account.margin_ratio)
        self.assertEqual("", account.margin_call_status)
        self.assertEqual(UNIX_EPOCH, account.last_updated)
