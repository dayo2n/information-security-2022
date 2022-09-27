#ifndef _SDES_
#define _SDES_

#include <cassert>
#include <cstring>

namespace S_DES {
    /* Simplified DES Implementation
     * Implemented at June 11, 2018 with C/C++
     */

#define P10(data)                   BOX_PASS(p10b, data, 10)
#define IP(data)                    BOX_PASS(ip, data, 8)
#define IP_1(data)                  BOX_PASS(ip_1, data, 8)
#define P8(data)                    BOX_PASS(p8b, data, 8)
#define P4(data)                    BOX_PASS(p4b, data, 4);

#define LS1(_key)                   ROTATE_LEFT(_key, 0, 4); ROTATE_LEFT(_key, 5, 9)
#define LS2(_key)                   LS1(_key); LS1(_key)
#define CREATE_KEY(_key, _k1, _k2)  P10(_key); \
                                    LS1(_key); memcpy(_k1, _key, 8); P8(_k1); \
                                    LS2(_key); memcpy(_k2, _key, 8); P8(_k2)


    using SDESBIT = __int8;
    using BITSET = SDESBIT [] ;
    using SBOX = SDESBIT[4][4][2];

    SDESBIT key[11];
    SDESBIT pdata[9];
    
    SDESBIT const p10b[] = { 3, 5, 2, 7, 4, 10, 1, 9, 8, 6 };
    SDESBIT const p8b[] = { 6, 3, 7, 4, 8, 5, 10, 9 };
    SDESBIT const p4b[] = { 2, 4, 3, 1 };
    SDESBIT const ip[] = { 2, 6, 3, 1, 4, 8, 5, 7 };
    SDESBIT const ip_1[] = { 4, 1, 3, 5, 7, 2, 8, 6 };
    SDESBIT const ep[] = { 4, 1, 2, 3, 2, 3, 4, 1 };
    
    SBOX const s0 = {
        { {'0', '1'}, {'0', '0'}, {'1', '1'}, {'1', '0'} },
        { {'1', '1'}, {'1', '0'}, {'0', '1'}, {'0', '0'} },
        { {'0', '0'}, {'1', '0'}, {'0', '1'}, {'1', '1'} },
        { {'1', '1'}, {'0', '1'}, {'1', '1'}, {'1', '0'} }
    };

    SBOX const s1 = {
        { {'0', '0'}, {'0', '1'}, {'1', '0'}, {'1', '1'} },
        { {'1', '0'}, {'0', '0'}, {'0', '1'}, {'1', '1'} },
        { {'1', '1'}, {'0', '0'}, {'0', '1'}, {'0', '0'} },
        { {'1', '0'}, {'0', '1'}, {'0', '0'}, {'1', '1'} }
    };

    // ----- INLINE FUNCTIONS  ------------------------------------------

    inline __int8 CTI(SDESBIT _bit) {
        return _bit - 48;
    }

    // ----- UTILITY FUNCTIONS ------------------------------------------
    
    void BIT_SWAP(
        BITSET data, 
        const int idx_a, 
        const int idx_b
    ) {
        data[idx_a] ^= data[idx_b];
        data[idx_b] ^= data[idx_a];
        data[idx_a] ^= data[idx_b];
    }

    void BIT_XOR(
        BITSET const a, 
        BITSET const b, 
        BITSET out
    ) {
        for (int i = 0; i < sizeof(a); ++i) {
            out[i] = a[i] ^ b[i];
        }
    }

    void BOX_PASS(
        BITSET const box, 
        BITSET data, 
        const int box_size
    ) {
        for (int i = 0; i < box_size; ++i) {
            BIT_SWAP(data, i, box[i]);
        }
    }

    void BOX_EXPAND(
        BITSET const expand_box,
        BITSET const source,
        BITSET out
    ) {
        for (int i = 0; i < 8; ++i) {
            out[i] = source[ expand_box[i] ];
        }
    }

    void ROTATE_LEFT(
        BITSET arr, 
        const int begin, 
        const int end
    ) {
        const int rotate_init = arr[begin];
        
        for (int i = begin + 1; i <= end; ++i) {
            arr[i - 1] = arr[i];
        }

        arr[end] = rotate_init;
    }

    void SWITCH(
        BITSET data
    ) {
        SDESBIT temp[4];
        memcpy(temp, data, 4);
        memcpy(data, data + 4, 4);
        memcpy(data + 4, data, 4);
    }

    // ----- Fk FUNCTION         ----------------------------------------

    void Fk(
        SDESBIT const data[8],
        BITSET const key,
        BITSET out
    ) {
        char left[4], right[4], right_ep[8], right_kep[8], p4[4];
        memcpy(left, data, 4);
        memcpy(right, data + 4, 4);

        BOX_EXPAND(ep, right, right_ep);
        BIT_XOR(right_ep, key, right_kep);

        memcpy(p4, 
            s0[CTI(right_kep[0]) * 2 + CTI(right_kep[3])][CTI(right_kep[1]) * 2 + CTI(right_kep[2])], 2);
        memcpy(p4 + 2, 
            s0[CTI(right_kep[0]) * 2 + CTI(right_kep[3])][CTI(right_kep[1]) * 2 + CTI(right_kep[2])], 2);
        BOX_PASS(p4b, p4, 4);

        BIT_XOR(left, p4, out);
        memcpy(out + 4, right, 4);
    }


    // ----- USER CALL FUNCTIONS ----------------------------------------

    void Encrypt(
        SDESBIT plain[8], 
        SDESBIT key[10]
    ) {
        char k1[8], k2[8], temp[8];
        CREATE_KEY(key, k1, k2);

        IP(plain);
        Fk(plain, k1, temp);
        SWITCH(temp);
        Fk(temp, k2, plain);
        IP_1(plain);
    }

    void Decrypt(
        SDESBIT crypt[8],
        SDESBIT key[10]
    ) {
        char k1[8], k2[8], temp[8];
        CREATE_KEY(key, k1, k2);

        IP(crypt);
        Fk(crypt, k2, temp);
        SWITCH(temp);
        Fk(temp, k1, crypt);
        IP_1(crypt);
    }

}

#endif
