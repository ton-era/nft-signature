import decimal

from tonsdk.utils import Address, to_nano, b64str_to_hex
from tonsdk.boc import Cell

from .utils import addr_from_b64
from .contract import Contract


class NFTSignature(Contract):
    code = 'B5EE9C7241021401000248000114FF00F4A413F4BCF2C80B0102016202030202CC04050029A14BC3E007F083F085F087F089F08BF08DF091F0930201200607020148101102012008090201200A0B00B3420C700925F04E001D0D3030171B0925F04E0FA4030F003F844C0009301F007E03381038C820898968013BE12F2F4D31F8102BD5220BA9331F008E0821005138D915220BA9331F00AE08102BE12BA92F009E05B8200FFFFF2F0800A35ED44D0FA4001F861FA4001F862FA4001F86320D749C0009D3070F86470F86570F86670F867E0D31F01F864D31F01F865D31F01F86620D749C200F867F84799D31F01F868D430F869973070F8686DF869E280201200C0D0201200E0F00513E11BE117E11323E1073C5BE10B3C5BE10F3C5B2C7F2C7F2C7FE11E63E127E121632C7F337B27B552000533E117E11AC775C2040AFC860043232C17E1073C5887E80B2DAB2C7F2CFFE10B3C5BE10F3C5B25C7EC02000892040E27E1170803CBCB4CFFE900C1C08208417F30F450860043232C17E10B3C5887E80B2DAB2C7C532CFC8B3C59633C584B280087E80B280325C7EC03E08FE197C017C0120004F0C2040E17E1044B1C17CBD2040E37E1130803CBCA040E2D6682082E4E1C02E7CBCBE08FE193C01200201201213001B4810387F84213C70512F2F4F006800B92040E1BE10C4F1C144BCBD2040E23E11B0803CBCB4C0007E19FE11E674C7C07E1A35007E1A77B4C0006389B4CFFE903E80350C2040AF1C20043232C1540173C59400FE8084F2DAB2C7C4B2CFF3325C7EC0244C38BE08FE19BC017C0120001B2040E2BE1084F1C144BCBD3C01A0ABFCB882'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def create_data_cell(self) -> Cell:
        cell = Cell()
        cell.bits.write_address(self.options['provider_address'])
        cell.bits.write_address(self.options['item_address'])
        cell.bits.write_address(self.options['signee_address'])

        return cell


    def create_init_payload(self):
        cell = Cell()
        cell.bits.write_uint(1, 1)  # any non empty body to handle init

        return cell


    # API

    def mint(self, 
               op_amount,
               wallet, client, send=True):
        state_init = self.create_state_init()['state_init']
        payload=self.create_init_payload()

        return self.api_call(wallet, client, op_amount, state_init, payload, send)



    # GET

    @Contract.getmethod
    def get_info(self, results):
        return {
            'provider_address': addr_from_b64(results[0][1]['object']['data']['b64'])['b'],
            'item_address':     addr_from_b64(results[1][1]['object']['data']['b64'])['b'],
            'signee_address':   addr_from_b64(results[2][1]['object']['data']['b64'])['b'],
            'time_created':        int(results[3][1], 16),
            'time_owner_approve':  int(results[4][1], 16),
            'time_signee_approve': int(results[5][1], 16),
            'payload_code': int(results[6][1], 16),
            'payload':      results[7][1],
        }
