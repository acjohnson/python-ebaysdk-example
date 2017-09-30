# -*- coding: utf-8 -*-
'''
© 2012-2013 eBay Software Foundation
Authored by: Tim Keefer
Licensed under CDDL 1.0
'''

import os
import sys
import datetime
from optparse import OptionParser

sys.path.insert(0, '%s/../' % os.path.dirname(__file__))

from common import dump

import ebaysdk
from ebaysdk.utils import getNodeText
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading


def init_options():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enabled debugging [default: %default]")
    parser.add_option("-y", "--yaml",
                      dest="yaml", default='ebay.yaml',
                      help="Specifies the name of the YAML defaults file. [default: %default]")
    parser.add_option("-a", "--appid",
                      dest="appid", default=None,
                      help="Specifies the eBay application id to use.")
    parser.add_option("-p", "--devid",
                      dest="devid", default=None,
                      help="Specifies the eBay developer id to use.")
    parser.add_option("-c", "--certid",
                      dest="certid", default=None,
                      help="Specifies the eBay cert id to use.")

    (opts, args) = parser.parse_args()
    return opts, args


def AddItem(opts):
    """http://www.utilities-online.info/xmltojson/#.UXli2it4avc
    """

    try:
        api = Trading(debug=opts.debug, config_file=opts.yaml, appid=opts.appid,
                      certid=opts.certid, devid=opts.devid, warnings=False)

        myitem = {
            "Item": {
                "Title": "Harry Potter and the Goblet of Fire",
                "Description": "This is the fourth book in the Harry Potter series. In very bad condition!",
                "PrimaryCategory": {"CategoryID": "377"},
                "StartPrice": "100.0",
                "BuyItNowPrice": "150.0",
                "CategoryMappingAllowed": "true",
                "Country": "US",
                "ConditionID": "3000",
                "Currency": "USD",
                "DispatchTimeMax": "3",
                "ListingDuration": "Days_7",
                "ListingType": "FixedPriceItem",
                "PaymentMethods": "PayPal",
                "PayPalEmailAddress": "fake@email.com",
                "PictureDetails": {"PictureURL": "http://i.ebayimg.com/00/s/NTAwWDM0NA==/z/7B0AAOSwE9RZyhg6/$_58.JPG"},
                "PostalCode": "52804",
                "Quantity": "1",
                "ReturnPolicy": {
                    "ReturnsAcceptedOption": "ReturnsAccepted",
                    "RefundOption": "MoneyBack",
                    "ReturnsWithinOption": "Days_30",
                    "Description": "If you are not satisfied, return the book for refund.",
                    "ShippingCostPaidByOption": "Buyer"
                },
                "SellerProfiles": {
                    "SellerPaymentProfile": {
                        "PaymentProfileName": "PayPal:Immediate pay",
                    },
                    "SellerReturnProfile": {
                        "ReturnProfileName": "30 Day Return Policy",
                    },
                    "SellerShippingProfile": {
                        "ShippingProfileName": "USPS First Class, Priority, Priority Express Flat Rate Envelope",
                    }
                },
                "ShippingDetails": {
                    "ShippingType": "Calculated",
                    "ShippingServiceOptions": {
                        "ShippingServicePriority": "1",
                        "ShippingService": "USPSMedia"
                    },
                    "CalculatedShippingRate": {
                        "OriginatingPostalCode": "52804",
                        "PackagingHandlingCosts": "0.0",
                        "ShippingPackage": "PackageThickEnvelope",
                        "WeightMajor": "1",
                        "WeightMinor": "0"
                    }
                },
                "Site": "US"
            }
        }

        api.execute('AddFixedPriceItem', myitem)
        dump(api)

    except ConnectionError as e:
        print(e)
        print(e.response.dict())


if __name__ == "__main__":
    (opts, args) = init_options()

    print("Trading API Samples for version %s" % ebaysdk.get_version())

    AddItem(opts)
